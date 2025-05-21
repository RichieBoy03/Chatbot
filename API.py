import sqlite3
import os
import google.generativeai as genai  # Correct import

# Get the API key from environment variables
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API Key is missing. Set it as an environment variable.")

# Configure the API key
genai.configure(api_key=api_key)

# Create the generation configuration
generation_config = genai.types.GenerationConfig(
    temperature=1,
    top_p=0.95,
    top_k=40,
    max_output_tokens=8192,
)

# Initialize the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",  # Updated to latest correct model name
    generation_config=generation_config
)

# Generate a response
try:
    response = model.generate_content("Essay on AI")
    print(response.text)  # Use .text to get the generated content
except Exception as e:
    print(f"An error occurred: {e}")

def connect_to_database():
    return sqlite3.connect("college.db")

def get_course_fees(course_name):
    """
    Fetches all fee-related information for a given course from the database.
    Returns a list of answers or an empty list if not found.
    """
    conn = connect_to_database()
    cursor = conn.cursor()
    # Try to fetch all fee-related answers for the course
    cursor.execute(
        """
        SELECT answer FROM college_queries
        WHERE (question LIKE ? OR question LIKE ? OR question LIKE ?)
        AND (question LIKE '%fee%' OR question LIKE '%fees%' OR question LIKE '%charges%' OR question LIKE '%cost%')
        """,
        (f"%{course_name}%", f"%{course_name.lower()}%", f"%{course_name.upper()}%")
    )
    results = cursor.fetchall()
    conn.close()
    return [row[0] for row in results] if results else []

def get_course_info(course_name, keyword=None):
    """
    Fetches all information for a given course and optional keyword from the database.
    Returns a list of answers or an empty list if not found.
    """
    conn = connect_to_database()
    cursor = conn.cursor()
    if keyword:
        cursor.execute(
            """
            SELECT answer FROM college_queries
            WHERE (question LIKE ? OR question LIKE ? OR question LIKE ?)
            AND (question LIKE ?)
            """,
            (f"%{course_name}%", f"%{course_name.lower()}%", f"%{course_name.upper()}%", f"%{keyword}%")
        )
    else:
        cursor.execute(
            """
            SELECT answer FROM college_queries
            WHERE (question LIKE ? OR question LIKE ? OR question LIKE ?)
            """,
            (f"%{course_name}%", f"%{course_name.lower()}%", f"%{course_name.upper()}%")
        )
    results = cursor.fetchall()
    conn.close()
    return [row[0] for row in results] if results else []

# Example usage:
if __name__ == "__main__":
    # Example: Fetch all fee info for BCA
    course = "BCA"
    fee_answers = get_course_fees(course)
    if fee_answers:
        print(f"Fee details for {course}:")
        for ans in fee_answers:
            print("-", ans)
    else:
        print(f"No fee details found for {course}.")

    # Example: Fetch all info for BCOM with keyword 'admission'
    course = "BCOM"
    keyword = "admission"
    info_answers = get_course_info(course, keyword)
    if info_answers:
        print(f"\nAdmission info for {course}:")
        for ans in info_answers:
            print("-", ans)
    else:
        print(f"No admission info found for {course}.")
