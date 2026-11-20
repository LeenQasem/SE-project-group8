# Task: Update the Main Project README to Reflect the Database Implementation

You are working on our Event & Volunteer Management System university Software Engineering project.

The database implementation for Increment 1 has recently been added to the repository, but the original root `README.md` has not been updated to reflect these changes.

Your task is to update the **existing main README.md** so that it accurately documents the current state of the project, including the newly implemented database.

## 1. Inspect the Repository First

Before making changes, inspect:

- The existing root `README.md`.
- The complete database folder and its contents.
- `database/README.md`, if present.
- Database configuration files.
- Database schema and migrations.
- Database models and repositories.
- Database initialization and seed scripts.
- Database tests.
- `requirements.md`.
- `incremental_development_plan.md`.
- The existing project source code and folder structure.

Understand what has actually been implemented.

Do not assume that a feature exists just because it is mentioned in the requirements.

## 2. Update the Existing Root README

Modify the existing root-level `README.md`.

IMPORTANT:
- Do NOT create another README file.
- Do NOT replace the entire README with a completely different document.
- Preserve useful existing content, formatting, headings, and project information.
- Do NOT remove existing sections unless they are genuinely outdated.
- Integrate the new information naturally into the existing structure.
- Avoid unnecessary repetition.

## 3. Add or Update the Database Section

Include a clear database section covering:

### Database Technology
- Identify the actual database management system being used.
- Mention relevant database technologies, libraries, or ORM tools if applicable.
- Do not list technologies that are not actually used.

### Database Implementation
Briefly explain:
- The purpose of the database.
- Its current implementation scope (Increment 1).
- The main tables and entities currently implemented.
- The important relationships.
- How referential integrity and data constraints are handled.

### Database Folder Structure
Show the actual relevant database folder structure.

Explain the purpose of the important files and directories.

Do not invent filenames or directories.

### Database Setup and Initialization
Provide accurate, step-by-step instructions explaining how to:

1. Install or configure the necessary database dependencies.
2. Configure environment variables, if required.
3. Create or initialize the database.
4. Apply migrations or execute schema scripts.
5. Insert seed or sample data, if available.
6. Verify that the database is working.

Use the actual commands supported by the repository.

### Database Testing
Explain:
- How to execute database tests.
- What aspects of the database are tested.
- Any prerequisites for running the tests.

Only describe tests that actually exist.

## 4. Update the General Project Setup Instructions

Review the existing installation and execution instructions.

Make sure the main README explains how the database setup fits into the overall project setup.

If the application requires a database to run, make this dependency clear.

Ensure the instructions are consistent with the actual implementation.

## 5. Preserve the Incremental Development Structure

Our project follows an incremental development approach.

Make it clear that:

- The current database implementation supports Increment 1.
- Later increments will extend the existing database.
- The project is developed as one evolving system, not as separate independent applications.

Do not imply that future increments have already been implemented.

## 6. Link to Database-Specific Documentation

Keep `database/README.md` as the detailed database documentation if it exists.

The root README should provide a brief overview and include a relative link to the database-specific README.

For example:

`[Database Documentation](database/README.md)`

Avoid duplicating the entire database README inside the main README.

## 7. Formatting and Presentation

Make the README professional, clean, organized, and easy to navigate.

Requirements:
- Use appropriate Markdown headings.
- Use readable code blocks for commands.
- Use tables only when they improve clarity.
- Use relative links for repository files.
- Maintain consistent formatting.
- Ensure the README renders correctly on GitHub.
- Avoid excessive explanations and unnecessary decorative elements.

## 8. Accuracy and Verification

Before finishing:

- Verify every command against the actual repository.
- Verify all referenced paths and filenames exist.
- Verify that the documented database technology matches the implementation.
- Ensure no unimplemented functionality is presented as complete.
- Ensure existing project information has not been accidentally removed.
- Check that all relative documentation links are correct.

Do not modify database implementation files or unrelated project files.

## 9. Final Report

After updating the README, provide:

1. A summary of the changes made.
2. The sections added or modified.
3. Any outdated information corrected.
4. Confirmation that the database-specific README was preserved.
5. Confirmation that all referenced paths and commands were checked.

## Final Objective

Update the existing root `README.md` so that anyone visiting our GitHub repository can understand the project, its current development status, and how the newly implemented Increment 1 database fits into the application.

The result must accurately represent the actual repository without duplicating the database-specific documentation.