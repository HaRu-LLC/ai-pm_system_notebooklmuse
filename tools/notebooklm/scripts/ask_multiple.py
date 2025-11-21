#!/usr/bin/env python3
"""
Ask Multiple NotebookLM Notebooks
Cross-notebook analysis tool - asks the same question to multiple notebooks and aggregates results

Usage:
    # Ask all notebooks in library
    python ask_multiple.py --question "What are the main risks?" --all-notebooks

    # Ask specific notebooks
    python ask_multiple.py --question "GPU status?" --notebook-ids "id1,id2"

    # Show browser for debugging
    python ask_multiple.py --question "..." --all-notebooks --show-browser
"""

import argparse
import sys
from pathlib import Path
from typing import List, Dict, Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from ask_question import ask_notebooklm
from notebook_manager import NotebookLibrary


def ask_multiple_notebooks(
    question: str,
    notebook_ids: Optional[List[str]] = None,
    all_notebooks: bool = False,
    headless: bool = True
) -> Dict[str, Optional[str]]:
    """
    Ask the same question to multiple notebooks and collect results

    Args:
        question: Question to ask
        notebook_ids: List of specific notebook IDs (optional)
        all_notebooks: Ask all notebooks in library
        headless: Run browser in headless mode

    Returns:
        Dictionary mapping notebook_id -> answer (or None if failed)
    """
    library = NotebookLibrary()

    # Determine target notebooks
    if all_notebooks:
        notebooks = library.list_notebooks()
        if not notebooks:
            print("❌ No notebooks in library")
            return {}
    elif notebook_ids:
        notebooks = []
        for nb_id in notebook_ids:
            nb = library.get_notebook(nb_id)
            if nb:
                notebooks.append(nb)
            else:
                print(f"⚠️  Notebook '{nb_id}' not found - skipping")
    else:
        print("❌ Must specify either --notebook-ids or --all-notebooks")
        return {}

    if not notebooks:
        print("❌ No valid notebooks to query")
        return {}

    print(f"\n🔍 Querying {len(notebooks)} notebook(s) with question:")
    print(f"   \"{question}\"\n")
    print("=" * 80)

    results = {}

    for i, notebook in enumerate(notebooks, 1):
        notebook_id = notebook['id']
        notebook_name = notebook['name']
        notebook_url = notebook['url']

        print(f"\n📓 [{i}/{len(notebooks)}] {notebook_name}")
        print(f"    ID: {notebook_id}")
        print("-" * 80)

        try:
            # Ask the question (without FOLLOW_UP_REMINDER)
            answer = ask_notebooklm(
                question=question,
                notebook_url=notebook_url,
                headless=headless
            )

            if answer:
                # Remove the FOLLOW_UP_REMINDER from individual answers
                # We'll add it once at the end
                if "EXTREMELY IMPORTANT: Is that ALL you need to know?" in answer:
                    answer = answer.split("EXTREMELY IMPORTANT: Is that ALL you need to know?")[0].strip()

                results[notebook_id] = {
                    'name': notebook_name,
                    'answer': answer,
                    'status': 'success'
                }
                print(f"✅ Got answer from {notebook_name}")
            else:
                results[notebook_id] = {
                    'name': notebook_name,
                    'answer': None,
                    'status': 'failed'
                }
                print(f"❌ Failed to get answer from {notebook_name}")

        except Exception as e:
            results[notebook_id] = {
                'name': notebook_name,
                'answer': None,
                'status': 'error',
                'error': str(e)
            }
            print(f"❌ Error querying {notebook_name}: {e}")

    return results


def format_results(question: str, results: Dict[str, Dict]) -> str:
    """
    Format the aggregated results for display

    Args:
        question: The question that was asked
        results: Dictionary of results from ask_multiple_notebooks

    Returns:
        Formatted string for display
    """
    output = []
    output.append("=" * 80)
    output.append(f"CROSS-NOTEBOOK ANALYSIS")
    output.append("=" * 80)
    output.append(f"\nQuestion: {question}\n")
    output.append(f"Notebooks queried: {len(results)}")

    successful = sum(1 for r in results.values() if r['status'] == 'success')
    output.append(f"Successful responses: {successful}/{len(results)}\n")
    output.append("=" * 80)

    # Display answers from each notebook
    for i, (notebook_id, result) in enumerate(results.items(), 1):
        output.append(f"\n## [{i}] {result['name']}")
        output.append(f"ID: {notebook_id}")
        output.append("-" * 80)

        if result['status'] == 'success':
            output.append(result['answer'])
        elif result['status'] == 'failed':
            output.append("❌ Failed to retrieve answer")
        else:  # error
            output.append(f"❌ Error: {result.get('error', 'Unknown error')}")

        output.append("")

    output.append("=" * 80)
    output.append("\n💡 CROSS-NOTEBOOK INSIGHTS:")
    output.append("The above responses come from different notebooks in your library.")
    output.append("Claude Code can now synthesize these answers to provide unified insights.\n")

    # Add follow-up reminder at the end
    output.append("EXTREMELY IMPORTANT: Is that ALL you need to know? ")
    output.append("You can always ask another question! Think about it carefully: ")
    output.append("before you reply to the user, review their original request and these answers. ")
    output.append("If anything is still unclear or missing, ask me another comprehensive question ")
    output.append("that includes all necessary context.")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description='Ask the same question to multiple NotebookLM notebooks',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Query all notebooks
  python ask_multiple.py --question "What are the main risks?" --all-notebooks

  # Query specific notebooks
  python ask_multiple.py --question "GPU status?" --notebook-ids "id1,id2"

  # Show browser
  python ask_multiple.py --question "..." --all-notebooks --show-browser
        """
    )

    parser.add_argument('--question', required=True, help='Question to ask all notebooks')
    parser.add_argument('--notebook-ids', help='Comma-separated list of notebook IDs')
    parser.add_argument('--all-notebooks', action='store_true', help='Query all notebooks in library')
    parser.add_argument('--show-browser', action='store_true', help='Show browser windows')

    args = parser.parse_args()

    # Parse notebook IDs if provided
    notebook_ids = None
    if args.notebook_ids:
        notebook_ids = [nid.strip() for nid in args.notebook_ids.split(',')]

    # Validate arguments
    if not args.all_notebooks and not notebook_ids:
        parser.error("Must specify either --all-notebooks or --notebook-ids")
        return 1

    # Ask multiple notebooks
    results = ask_multiple_notebooks(
        question=args.question,
        notebook_ids=notebook_ids,
        all_notebooks=args.all_notebooks,
        headless=not args.show_browser
    )

    if not results:
        print("\n❌ No results to display")
        return 1

    # Format and display results
    formatted_output = format_results(args.question, results)
    print("\n" + formatted_output)

    # Return success if at least one notebook answered successfully
    successful = sum(1 for r in results.values() if r['status'] == 'success')
    return 0 if successful > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
