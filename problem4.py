"""
Problem 4: Data Persistence with JSON
Learn to use Python modules (imports) and save data to files using JSON.
"""

import json
import os


def save_to_json(data, filename):
    """
    Save data to a JSON file.

    Args:
        data: Python data structure (list, dict, etc.)
        filename (str): Name of file to save to

    Returns:
        bool: True if successful, False if error occurred

    Example:
        >>> data = {'name': 'Alice', 'age': 25}
        >>> save_to_json(data, 'test.json')
        True
    """

    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception:
        return False


def load_from_json(filename):
    """
    Load data from a JSON file.

    Args:
        filename (str): Name of file to load from

    Returns:
        Data from file if successful, None if error occurred

    Example:
        >>> data = load_from_json('test.json')
        >>> data
        {'name': 'Alice', 'age': 25}
    """

    try:
        with open(filename, "r") as f:
            data = json.load(f)
            return data
    except Exception:
        return None


def save_contacts_to_file(contacts, filename="contacts.json"):
    """
    Save a list of contacts to a JSON file.

    Args:
        contacts (list): List of contact dictionaries
        filename (str): File to save to (default: contacts.json)

    Returns:
        bool: True if successful, False otherwise
    """

    return save_to_json(contacts, filename)


def load_contacts_from_file(filename="contacts.json"):
    """
    Load contacts from a JSON file.

    Args:
        filename (str): File to load from (default: contacts.json)

    Returns:
        list: List of contacts, or empty list if file doesn't exist
    """

    if load_from_json(filename) is None:
        return []

    return load_from_json(filename)


def append_contact_to_file(contact, filename="contacts.json"):
    """
    Load existing contacts, add a new contact, and save back to file.

    Args:
        contact (dict): Contact dictionary to add
        filename (str): File to use

    Returns:
        bool: True if successful
    """

    rep = load_contacts_from_file(filename)
    rep.append(contact)
    return save_contacts_to_file(rep, filename)


def backup_file(source_filename, backup_filename):
    """
    Create a backup copy of a file.

    Args:
        source_filename (str): Original file
        backup_filename (str): Backup file name

    Returns:
        bool: True if successful
    """

    try:
        with open(source_filename, "r") as f:
            data = json.load(f)
            save_to_json(data, backup_filename)
            return True
    except Exception:
        return False


def get_file_stats(filename):
    """
    Get statistics about a JSON file.

    Args:
        filename (str): File to analyze

    Returns:
        dict or None: Dictionary with keys:
            - 'exists': bool
            - 'type': 'list' or 'dict' or 'other'
            - 'count': number of items (if list) or keys (if dict)
            - 'size_bytes': file size in bytes

    Example:
        >>> get_file_stats('contacts.json')
        {'exists': True, 'type': 'list', 'count': 5, 'size_bytes': 1234}
    """

    try:
        data = load_from_json(filename)
        stat = {
            "exists": os.path.exists(filename),
            "type": type(data).__name__,
            "count": len(data),
            "size_bytes": os.path.getsize(filename),
        }
        return stat
    except Exception:
        return None


def merge_json_files(file1, file2, output_file):
    """
    Merge two JSON files containing lists.

    Args:
        file1 (str): First file
        file2 (str): Second file
        output_file (str): Output file

    Returns:
        bool: True if successful

    Example:
        If file1.json has [1, 2, 3] and file2.json has [4, 5],
        output_file.json will have [1, 2, 3, 4, 5]
    """

    if not os.path.exists(file1) or not os.path.exists(file2):
        return None

    data1, data2 = load_from_json(file1), load_from_json(file2)

    if isinstance(data1, list) and isinstance(data2, list):
        final_list = data1 + data2
        save_to_json(final_list, output_file)
        return True

    return None


def search_json_file(filename, key, value):
    """
    Search a JSON file (containing a list of dicts) for items matching a key-value pair.

    Args:
        filename (str): JSON file to search
        key (str): Key to search for
        value: Value to match

    Returns:
        list: List of matching items

    Example:
        If file has [{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}]
        search_json_file('data.json', 'name', 'Alice')
        returns [{'name': 'Alice', 'age': 25}]
    """

    data = load_from_json(filename)
    matches = []
    for i in data:
        if i.get(key) == value:
            matches.append(i)

    return matches


# Test cases
if __name__ == "__main__":
    print("Testing JSON File Operations...")
    print("-" * 50)

    # Test 1: save_to_json and load_from_json
    print("Test 1: save_to_json and load_from_json")
    test_data = {"name": "Alice", "age": 25, "city": "Paris"}
    save_to_json(test_data, "test_data.json")
    loaded_data = load_from_json("test_data.json")
    print(f"Saved and loaded: {loaded_data}")
    assert loaded_data == test_data
    print("✓ Passed\n")

    # Test 2: save_contacts_to_file and load_contacts_from_file
    print("Test 2: save and load contacts")
    contacts = [
        {"name": "Alice", "phone": "555-0001", "email": "alice@email.com"},
        {"name": "Bob", "phone": "555-0002", "email": "bob@email.com"},
    ]
    save_contacts_to_file(contacts, "test_contacts.json")
    loaded_contacts = load_contacts_from_file("test_contacts.json")
    print(f"Loaded {len(loaded_contacts)} contacts")
    assert len(loaded_contacts) == 2
    assert loaded_contacts[0]["name"] == "Alice"
    print("✓ Passed\n")

    # Test 3: append_contact_to_file
    print("Test 3: append_contact_to_file")
    new_contact = {"name": "Charlie", "phone": "555-0003", "email": "charlie@email.com"}
    append_contact_to_file(new_contact, "test_contacts.json")
    contacts = load_contacts_from_file("test_contacts.json")
    print(f"After append: {len(contacts)} contacts")
    assert len(contacts) == 3
    print("✓ Passed\n")

    # Test 4: backup_file
    print("Test 4: backup_file")
    backup_file("test_contacts.json", "test_contacts_backup.json")
    backup_data = load_from_json("test_contacts_backup.json")
    print(f"Backup created with {len(backup_data)} items")
    assert len(backup_data) == 3
    print("✓ Passed\n")

    # Test 5: get_file_stats
    print("Test 5: get_file_stats")
    stats = get_file_stats("test_contacts.json")
    print(f"File stats: {stats}")
    assert stats is not None
    assert stats["exists"] == True
    assert stats["type"] == "list"
    assert stats["count"] == 3
    print("✓ Passed\n")

    # Test 6: merge_json_files
    print("Test 6: merge_json_files")
    list1 = [1, 2, 3]
    list2 = [4, 5, 6]
    save_to_json(list1, "list1.json")
    save_to_json(list2, "list2.json")
    merge_json_files("list1.json", "list2.json", "merged.json")
    merged = load_from_json("merged.json")
    print(f"Merged list: {merged}")
    assert merged == [1, 2, 3, 4, 5, 6]
    print("✓ Passed\n")

    # Test 7: search_json_file
    print("Test 7: search_json_file")
    results = search_json_file("test_contacts.json", "name", "Alice")
    print(f"Search results: {results}")
    assert len(results) == 1
    assert results[0]["name"] == "Alice"
    print("✓ Passed\n")

    # Cleanup
    print("Cleaning up test files...")
    import os

    for file in [
        "test_data.json",
        "test_contacts.json",
        "test_contacts_backup.json",
        "list1.json",
        "list2.json",
        "merged.json",
    ]:
        if os.path.exists(file):
            os.remove(file)
    print("✓ Cleaned up\n")

    print("=" * 50)
    print("All tests passed! You've mastered JSON file operations!")
