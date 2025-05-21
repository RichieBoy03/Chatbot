import sqlite3

def setup_database():
    """Creates database tables and inserts sample data."""
    conn = sqlite3.connect("college.db")
    cursor = conn.cursor()

    # Create table for college queries
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS college_queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT UNIQUE,
            answer TEXT
        )
    ''')

    # Insert sample queries
    sample_data = [
        # General Queries
        ("What is the name of the college?", "The name of the college is Don Bosco College, K R Puram."),
        ("Where is the college located?", "Don Bosco College is located in K R Puram, Bengaluru."),
        ("What are the admission requirements?", "You need to submit your 12th-grade mark sheet and entrance exam score."),
        ("Where can I get my ID card?", "You can collect your ID card from the admin office."),
        ("What is the college timing?", "College operates from 9:00 AM to 3:00 PM."),
        ("Who is the principal?", "The principal of the college is Father Geo."),
        ("What UG programs are offered?", "BCA, BBA, B.Com, BA, BSW"),
        ("What PG programs are offered?", "MA, MSW, M.Com"),
        ("Is hostel facility available?", "Yes, hostel facility is available for both boys and girls."),

        # Fee structure queries
        ("What is the fee structure for BCA?", "The semester-wise fee for BCA is ₹50,000 per semester. Additional fees: Library ₹2,000, Lab ₹3,000, Exam ₹2,500."),
        ("What is the fee structure for BBA?", "The semester-wise fee for BBA is ₹45,000 per semester. Additional fees: Library ₹2,000, Lab ₹3,000, Exam ₹2,500."),
        ("What is the fee structure for B.Com?", "The semester-wise fee for B.Com is ₹40,000 per semester. Additional fees: Library ₹2,000, Lab ₹3,000, Exam ₹2,500."),
        ("What is the fee structure for BA?", "The semester-wise fee for BA is ₹25,000 per semester. Additional fees: Library ₹2,000, Lab ₹3,000, Exam ₹2,500."),
        ("What is the fee structure for BSW?", "The semester-wise fee for BSW is ₹30,000 per semester. Additional fees: Library ₹2,000, Lab ₹3,000, Exam ₹2,500."),
        ("What is the fee structure for MA?", "The semester-wise fee for MA is ₹25,000 per semester. Additional fees: Library ₹2,000, Lab ₹3,000, Exam ₹2,500."),
        ("What is the fee structure for MSW?", "The semester-wise fee for MSW is ₹30,000 per semester. Additional fees: Library ₹2,000, Lab ₹3,000, Exam ₹2,500."),
        ("What is the fee structure for M.Com?", "The semester-wise fee for M.Com is ₹30,000 per semester. Additional fees: Library ₹2,000, Lab ₹3,000, Exam ₹2,500."),

        # Additional Fees Queries
        ("What are the additional fees?", "Library Fee: ₹2,000, Lab Fee: ₹3,000, Sports Fee: ₹1,500, Exam Fee: ₹2,500, Hostel Fee: ₹50,000, Uniform Fee (First Year Only): ₹6,000, Non-Karnataka Students Additional Fee: ₹10,000, Exam Registration Fee: As notified by the university."),
        ("How much is the library fee?", "The library fee is ₹2,000 per year."),
        ("What is the lab fee?", "The lab fee is ₹3,000 per year."),
        ("How much is the sports fee?", "The sports fee is ₹1,500 per year."),
        ("How much is the exam fee?", "The exam fee is ₹2,500 per semester."),
        ("What is the hostel fee?", "The hostel fee is ₹50,000 per year."),
        ("How much is the uniform fee?", "The uniform fee is ₹6,000 (only for first-year students)."),
        ("Is there any additional fee for non-Karnataka students?", "Yes, non-Karnataka students need to pay an additional fee of ₹10,000."),
        ("How much is the exam registration fee?", "The exam registration fee is as notified by the university each semester."),

        # Scholarship Queries
        ("What is the scholarship criteria?", "25% fee waiver for 95%+ in university exams + 90% attendance, 20% for 90%+, 15% for 85%+."),
        ("How much fee waiver is given for 95% marks?", "If you score 95% in university exams and have 90% attendance, you get a 25% fee waiver."),
        ("How much fee waiver is given for 90% marks?", "If you score 90% in university exams and have 90% attendance, you get a 20% fee waiver."),
        ("How much fee waiver is given for 85% marks?", "If you score 85% in university exams and have 90% attendance, you get a 15% fee waiver.")
    ]

    cursor.executemany("INSERT OR IGNORE INTO college_queries (question, answer) VALUES (?, ?)", sample_data)

    # Create table for additional fees
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS additional_fees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fee_type TEXT,
            amount TEXT
        )
    ''')

    additional_fees_data = [
        ("Library Fee", 2000),
        ("Lab Fee", 3000),
        ("Sports Fee", 1500),
        ("Exam Fee", 2500),
        ("Hostel Fee", 50000),
        ("Uniform Fee (First Year Only)", 6000),
        ("Non-Karnataka Students Additional Fee", 10000),
    ]

    cursor.executemany("INSERT OR IGNORE INTO additional_fees (fee_type, amount) VALUES (?, ?)", additional_fees_data)

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("✅ Database setup completed")

# Ensure the function runs only when executed directly
if __name__ == "__main__":
    setup_database()
# Output: ✅ Database setup completed
# The setup_database function creates two tables in the college.db database: college_queries and additional_fees.