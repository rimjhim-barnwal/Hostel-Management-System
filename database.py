"""
models/fee.py
-------------
Fee model — handles payment recording and reporting.
"""

from database import Database


class Fee:
    """Tracks and reports fee payments for hostel students."""

    def __init__(self, db: Database):
        self.db = db

    def record_payment(self, student_id: int, amount: float,
                       remarks: str = "") -> int:
        """Insert a fee payment and update the student's fee_status to 'Paid'."""
        payment_id = self.db.execute(
            """INSERT INTO fee_records (student_id, amount, remarks)
               VALUES (%s, %s, %s)""",
            (student_id, amount, remarks)
        )
        # Auto-mark as paid after a payment is recorded
        self.db.execute(
            "UPDATE students SET fee_status = 'Paid' WHERE id = %s",
            (student_id,)
        )
        return payment_id

    def get_history(self, student_id: int) -> list:
        """All payment records for one student, newest first."""
        return self.db.fetchall(
            """SELECT fr.*, s.name AS student_name
               FROM fee_records fr
               JOIN students s ON s.id = fr.student_id
               WHERE fr.student_id = %s
               ORDER BY fr.payment_date DESC""",
            (student_id,)
        )

    def pending_students(self) -> list:
        """Students whose fee_status is not 'Paid'."""
        return self.db.fetchall(
            """SELECT id, name, room_number, phone, fee_status
               FROM students
               WHERE fee_status != 'Paid'
               ORDER BY fee_status, name"""
        )

    def total_collected(self) -> float:
        """Sum of all payments ever recorded."""
        row = self.db.fetchone("SELECT COALESCE(SUM(amount), 0) AS total FROM fee_records")
        return float(row["total"])
