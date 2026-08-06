# Student Registration Portal 🎓

A modern, role-based web application built with **ASP.NET Core 10.0 MVC**, **ASP.NET Core Identity**, and **Entity Framework Core** using **Microsoft SQL Server**.

---

## ⚡ Highlights & Key Features

* **Individual Accounts Authentication**: Secure registration, login, logout, and password hashing via ASP.NET Core Identity.
* **Role-Based Access Control (RBAC)**:
  * **Administrator**: Manage course catalog (Create, Read, Update, Delete) and view complete student roster.
  * **Student**: Browse courses, register for a course (enforced **1 course limit**), view & edit personal profile.
* **Dynamic Role-Based Navigation**: Navbar automatically adjusts links depending on role (`Admin`, `Student`, or `Anonymous`). Automatically hides course registration links after enrollment.
* **Automated Database Creation & Seeding**: Auto-creates `StudentRegistrationDb` on SQL Server (`SQLEXPRESS`) and seeds:
  * Default roles: `Admin` and `Student`
  * Default Admin account: `admin@studentreg.com`
  * 5 Initial Academic Courses
* **Modern Glassmorphic UI**: Styled with Google Fonts (Inter), Bootstrap 5, custom CSS glassmorphism, responsive cards, and real-time status banners.

---

## 🛠️ Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Framework** | ASP.NET Core 10.0 (MVC Pattern) |
| **Security / Auth** | ASP.NET Core Identity (Cookie Authentication & RBAC) |
| **ORM / Data Access** | Entity Framework Core 10.0 |
| **Database** | Microsoft SQL Server Express (`SQLEXPRESS`) |
| **UI & Styling** | Razor Views, Bootstrap 5, Bootstrap Icons, Custom CSS |

---

## 🔐 Access Control Matrix

| Feature / Page | Anonymous | Student | Administrator |
| :--- | :---: | :---: | :---: |
| Home & Course Directory | ✅ Read | ✅ Read | ✅ Read |
| Account Registration | ✅ Sign Up | ❌ | ❌ |
| Enroll in Course | ❌ | ✅ (Max 1) | ❌ |
| Personal Profile View/Edit | ❌ | ✅ | ❌ |
| Manage Courses (Create/Edit/Delete) | ❌ | ❌ | ✅ |
| View Student Roster | ❌ | ❌ | ✅ |

---

## 🔑 Pre-Seeded Test Credentials

| Role | Email | Password |
| :--- | :--- | :--- |
| **Administrator** | `admin@studentreg.com` | `AdminPassword123!` |
| **Student** | *Self-register via UI* | *Set upon signup* |

---

## 🚀 Quick Start (Running Locally)

### Prerequisites
* [.NET 10.0 SDK](https://dotnet.microsoft.com/)
* [SQL Server Express](https://www.microsoft.com/en-us/sql-server/sql-server-downloads) (`SQLEXPRESS`)

### Run via Command Line
```powershell
# Navigate to project root
cd "c:\MP Online"

# Restore dependencies & run server
dotnet run --launch-profile "http"
```

Open your browser and navigate to: **`http://localhost:5219`**

### Run via Visual Studio
1. Open `StudentRegistration.sln` in Visual Studio 2022.
2. Press **F5** or click **Start (http)**.

---

## 📁 Repository Structure

```text
├── Controllers/
│   ├── AccountController.cs    # Auth, Register, Login, Logout, AccessDenied
│   ├── CoursesController.cs    # Course catalog CRUD
│   ├── ProfileController.cs    # Student profile & course enrollment
│   └── StudentsController.cs   # Admin student roster
├── Data/
│   ├── ApplicationDbContext.cs # EF Core DbContext mapping
│   └── DbInitializer.cs        # Auto-creation & seeding logic
├── Models/
│   ├── ApplicationUser.cs      # Extended IdentityUser model
│   ├── Course.cs               # Course entity
│   └── ViewModels.cs           # DTOs for login/register/profile
├── Views/
│   ├── Account/                # Login, Register, AccessDenied
│   ├── Courses/                # Index, Create, Edit, Delete
│   ├── Profile/                # Student profile & profile edit
│   ├── Students/               # Student roster table
│   └── Shared/_Layout.cshtml   # Dynamic role-based navigation bar
├── wwwroot/css/site.css        # Glassmorphic custom styling
├── Program.cs                  # Services DI & Pipeline setup
└── appsettings.json            # SQL Server connection string
```

---

## 📄 Submission Documents

* **[StudentRegistration_Assignment_Submission.docx](StudentRegistration_Assignment_Submission.docx)**: Formatted assignment document containing Part A (UI screenshots & DB schema) and Part B (complete source code).
* **[Combined_Source_Code.txt](Combined_Source_Code.txt)**: Single consolidated source code reference file.
