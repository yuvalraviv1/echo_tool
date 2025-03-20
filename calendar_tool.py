from mcp.server.fastmcp import FastMCP
from datetime import datetime
from typing import Dict, List
import json
import os

# Create an MCP server
mcp = FastMCP("calendar_tool")

# File to store calendar data
CALENDAR_FILE = "calendar_data.txt"

# Data structure to hold calendar data
calendar_data: Dict[str, List[str]] = {}


def _validate_date_format(date_str: str) -> bool:
    """Helper function to validate date format (YYYY-MM-DD)."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def _load_calendar_data():
    """Loads calendar data from the persistent file."""
    global calendar_data
    if os.path.exists(CALENDAR_FILE):
        try:
            with open(CALENDAR_FILE, "r") as f:
                calendar_data = json.load(f)
        except json.JSONDecodeError:
            print("Error decoding calendar data. Starting with an empty calendar.")
            calendar_data = {}
    else:
        calendar_data = {}


def _save_calendar_data():
    """Saves calendar data to the persistent file."""
    with open(CALENDAR_FILE, "w") as f:
        json.dump(calendar_data, f)


@mcp.tool()
def add_task(date: str, task: str) -> str:
    """
    Adds a task to a specific date in the calendar.

    Args:
        date (str): The date in YYYY-MM-DD format.
        task (str): The task description.

    Returns:
        str: A message indicating success or failure.
    """
    if not _validate_date_format(date):
        return "Invalid date format. Please use YYYY-MM-DD."

    if date not in calendar_data:
        calendar_data[date] = []
    calendar_data[date].append(task)
    _save_calendar_data()
    return f"Task '{task}' added to {date}."


@mcp.tool()
def remove_task(date: str, task: str) -> str:
    """
    Removes a task from a specific date in the calendar.

    Args:
        date (str): The date in YYYY-MM-DD format.
        task (str): The task description to remove.

    Returns:
        str: A message indicating success or failure.
    """
    if not _validate_date_format(date):
        return "Invalid date format. Please use YYYY-MM-DD."

    if date not in calendar_data:
        return f"No tasks found for {date}."

    if task in calendar_data[date]:
        calendar_data[date].remove(task)
        _save_calendar_data()
        return f"Task '{task}' removed from {date}."
    else:
        return f"Task '{task}' not found on {date}."


@mcp.tool()
def get_tasks(date: str) -> str:
    """
    Gets all tasks for a specific date.

    Args:
        date (str): The date in YYYY-MM-DD format.

    Returns:
        str: A list of tasks for the given date, or a message if no tasks are found or the date is invalid.
    """
    if not _validate_date_format(date):
        return "Invalid date format. Please use YYYY-MM-DD."
    if date not in calendar_data:
        return f"No tasks found for {date}."
    return f"Tasks for {date}: {', '.join(calendar_data[date])}"


@mcp.tool()
def get_all_tasks() -> str:
    """
    Gets all tasks for all dates.

    Returns:
        str: A list of tasks for all dates, or a message if no tasks are found.
    """
    if not calendar_data:
        return "No tasks found in the calendar."
    result = ""
    for date, tasks in calendar_data.items():
        result += f"Tasks for {date}: {', '.join(tasks)}\n"
    return result


if __name__ == "__main__":
    _load_calendar_data()  # Load data when the server starts
    mcp.run()
