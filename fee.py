"""
main.py
-------
Hostel Management System — menu-driven console application.
Entry point: run with  python main.py

Architecture:
    main.py         ← UI / menu loop
    database.py     ← DB connection wrapper
    models/         ← business logic (Student, Room, Fee)
    sql/schema.sql  ← DDL to initialise the DB
"""

import os
import sys
from database import Database
from models.student import Student
from models.room    import Room
from models.fee     import Fee

# ── Colour helpers (ANSI — fall back gracefully on Windows CMD) ───────────────
def clr(text, code): return f"\033[{code}m{text}\033[0m"
GREEN  = lambda t: clr(t, "92")
RED    = lambda t: clr(t, "91")
YELLOW = lambda t: clr(t, "93")
CYAN   = lambda t: clr(t, "96")
BOLD   = lambda t: clr(t, "1")

# ─────────────────────────────────────────────────────────────────────────────
#  Display helpers
# ─────────────────────────────────────────────────────────────────────────────

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    print(CYAN("=" * 60))
    print(CYAN("       🏠  HOSTEL MANAGEMENT SYSTEM  🏠"))
    print(CYAN("=" * 60))


def pause():
    input("\n  Press ENTER to continue…")


def print_student_table(students: list):
    """Pretty-print a list of student dicts."""
    if not students:
        print(YELLOW("  No records found."))
        return
    sep = "-" * 80
    print(sep)
    print(f"  {'ID':<5} {'Name':<22} {'Room':<8} {'Phone':<14} {'Course':<18} {'Fee':<8}")
    print(sep)
    for s in students:
        fee_col = GREEN(s["fee_status"]) if s["fee_status"] == "Paid" else RED(s["fee_status"])
        print(f"  {s['id']:<5} {s['name']:<22} {s['room_number']:<8} "
              f"{s['phone']:<14} {str(s['course'] or ''):<18} {fee_col}")
    print(sep)
    print(f"  Total: {len(students)} student(s)")


# ─────────────────────────────────────────────────────────────────────────────
#  Menu actions
# ─────────────────────────────────────────────────────────────────────────────

def menu_add_student(student_model: Student, room_model: Room):
    """Collect input and register a new student."""
    print(BOLD("\n  ── ADD NEW STUDENT ──"))

    # Show available rooms first
    available = room_model.get_available()
    if not available:
        print(RED("  No rooms available at the moment!"))
        return

    print(f"\n  Available rooms: ", end="")
    print(", ".join(r["room_number"] for r in available))

    name   = input("\n  Full Name     : ").strip()
    room   = input("  Room Number   : ").strip().upper()
    phone  = input("  Phone         : ").strip()
    email  = input("  Email         : ").strip()
    course = input("  Course        : ").strip()

    if not (name and room and phone):
        print(RED("  Name, room, and phone are required."))
        return

    try:
        sid = student_model.register(name, room, phone, email, course)
        print(GREEN(f"\n  ✔ Student registered successfully! (ID: {sid})"))
    except ValueError as e:
        print(RED(f"\n  ✘ {e}"))
    except Exception as e:
        print(RED(f"\n  ✘ Database error: {e}"))


def menu_view_students(student_model: Student):
    """Display every student."""
    print(BOLD("\n  ── ALL STUDENTS ──"))
    students = student_model.get_all()
    print_student_table(students)


def menu_search(student_model: Student):
    """Search by name, phone, or room."""
    print(BOLD("\n  ── SEARCH STUDENT ──"))
    keyword = input("  Enter name / phone / room: ").strip()
    if not keyword:
        return
    results = student_model.search(keyword)
    print_student_table(results)


def menu_update_student(student_model: Student):
    """Update name / phone / email / course of a student."""
    print(BOLD("\n  ── UPDATE STUDENT ──"))
    try:
        sid = int(input("  Enter Student ID: "))
    except ValueError:
        print(RED("  Invalid ID."))
        return

    student = student_model.get_by_id(sid)
    if not student:
        print(RED("  Student not found."))
        return

    print(f"\n  Editing: {student['name']} (Room {student['room_number']})")
    print("  Leave blank to keep current value.\n")

    name   = input(f"  Name   [{student['name']}]  : ").strip() or student["name"]
    phone  = input(f"  Phone  [{student['phone']}] : ").strip() or student["phone"]
    email  = input(f"  Email  [{student['email'] or ''}] : ").strip() or student["email"]
    course = input(f"  Course [{student['course'] or ''}] : ").strip() or student["course"]

    try:
        student_model.update(sid, name, phone, email, course)
        print(GREEN("  ✔ Student updated."))
    except Exception as e:
        print(RED(f"  ✘ {e}"))


def menu_delete_student(student_model: Student):
    """Delete a student after confirmation."""
    print(BOLD("\n  ── DELETE STUDENT ──"))
    try:
        sid = int(input("  Enter Student ID: "))
    except ValueError:
        print(RED("  Invalid ID."))
        return

    student = student_model.get_by_id(sid)
    if not student:
        print(RED("  Student not found."))
        return

    confirm = input(f"  Delete '{student['name']}' from room {student['room_number']}? (yes/no): ")
    if confirm.lower() != "yes":
        print(YELLOW("  Cancelled."))
        return

    try:
        student_model.delete(sid)
        print(GREEN("  ✔ Student deleted. Room freed."))
    except Exception as e:
        print(RED(f"  ✘ {e}"))


def menu_fee_management(student_model: Student, fee_model: Fee):
    """Sub-menu for fee operations."""
    while True:
        print(BOLD("\n  ── FEE MANAGEMENT ──"))
        print("  1. Record Payment")
        print("  2. Update Fee Status")
        print("  3. View Pending Students")
        print("  4. View Fee History (by Student ID)")
        print("  5. Total Collected")
        print("  0. Back")
        choice = input("\n  Choice: ").strip()

        if choice == "1":
            try:
                sid    = int(input("  Student ID  : "))
                amount = float(input("  Amount (₹)  : "))
                remark = input("  Remarks     : ").strip()
                fee_model.record_payment(sid, amount, remark)
                print(GREEN("  ✔ Payment recorded."))
            except Exception as e:
                print(RED(f"  ✘ {e}"))

        elif choice == "2":
            try:
                sid    = int(input("  Student ID  : "))
                status = input("  Status (Paid/Pending/Partial): ").strip().capitalize()
                student_model.update_fee_status(sid, status)
                print(GREEN("  ✔ Fee status updated."))
            except Exception as e:
                print(RED(f"  ✘ {e}"))

        elif choice == "3":
            pending = fee_model.pending_students()
            print_student_table(pending)

        elif choice == "4":
            try:
                sid     = int(input("  Student ID: "))
                history = fee_model.get_history(sid)
                if not history:
                    print(YELLOW("  No payment records."))
                else:
                    for h in history:
                        print(f"  [{h['payment_date']}]  ₹{h['amount']:.2f}  —  {h['remarks']}")
            except Exception as e:
                print(RED(f"  ✘ {e}"))

        elif choice == "5":
            total = fee_model.total_collected()
            print(GREEN(f"\n  Total fee collected: ₹{total:,.2f}"))

        elif choice == "0":
            break

        pause()


def menu_room_status(room_model: Room):
    """Show room availability summary."""
    print(BOLD("\n  ── ROOM STATUS ──"))
    summary = room_model.summary()
    print(f"  Total rooms  : {summary['total']}")
    print(GREEN(f"  Available    : {summary['available']}"))
    print(RED(f"  Occupied     : {summary['occupied']}"))

    show_all = input("\n  Show all rooms? (y/n): ").lower()
    if show_all == "y":
        rooms = room_model.get_all()
        print(f"\n  {'Room':<8} {'Type':<8} {'Floor':<6} {'Capacity':<10} {'Occupied'}")
        print("-" * 50)
        for r in rooms:
            status = RED("Yes") if r["occupied"] else GREEN("No")
            print(f"  {r['room_number']:<8} {r['type']:<8} {r['floor']:<6} "
                  f"{r['capacity']:<10} {status}")


# ─────────────────────────────────────────────────────────────────────────────
#  Main loop
# ─────────────────────────────────────────────────────────────────────────────

MENU = """
  ┌─────────────────────────────────┐
  │  1.  Add / Register Student     │
  │  2.  View All Students          │
  │  3.  Search Student             │
  │  4.  Update Student Info        │
  │  5.  Delete Student             │
  │  6.  Fee Management             │
  │  7.  Room Status                │
  │  0.  Exit                       │
  └─────────────────────────────────┘
"""

def main():
    clear_screen()
    print_header()
    print("\n  Connecting to database…")

    db = Database()
    student_model = Student(db)
    room_model    = Room(db)
    fee_model     = Fee(db)

    try:
        while True:
            clear_screen()
            print_header()
            print(MENU)
            choice = input("  Select option: ").strip()

            if choice == "1":
                menu_add_student(student_model, room_model)
            elif choice == "2":
                menu_view_students(student_model)
            elif choice == "3":
                menu_search(student_model)
            elif choice == "4":
                menu_update_student(student_model)
            elif choice == "5":
                menu_delete_student(student_model)
            elif choice == "6":
                menu_fee_management(student_model, fee_model)
            elif choice == "7":
                menu_room_status(room_model)
            elif choice == "0":
                print(YELLOW("\n  Goodbye! 👋\n"))
                break
            else:
                print(RED("  Invalid option. Please try again."))

            if choice != "0":
                pause()

    except KeyboardInterrupt:
        print(YELLOW("\n\n  Interrupted. Exiting…\n"))
    finally:
        db.close()


if __name__ == "__main__":
    main()
