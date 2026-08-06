# Help Desk Ticket Management System (`HelpDeskManagement`)

A complete Help Desk Ticket Management System built with **ASP.NET Core 10.0 Web API**, **Entity Framework Core**, **SQL Server**, **ASP.NET Core MVC** (consuming API via `HttpClient`), and **xUnit with Moq** for unit testing.

---

## 📁 Repository Structure

```
HelpDeskManagement/
├── HelpDesk.Api/
│   ├── Controllers/
│   │   └── TicketController.cs        # REST API endpoints
│   ├── Data/
│   │   └── HelpDeskDbContext.cs       # EF Core DbContext & seed data
│   ├── Models/
│   │   └── Ticket.cs                  # Primary Ticket domain entity
│   ├── Repositories/
│   │   ├── ITicketRepository.cs       # Repository interface
│   │   └── TicketRepository.cs        # Async Repository implementation
│   ├── Program.cs
│   └── appsettings.json
│
├── HelpDesk.Mvc/
│   ├── Controllers/
│   │   ├── HomeController.cs          # Redirects root to Dashboard
│   │   └── TicketController.cs        # MVC Controller for Dashboard, Index, Create, Edit, Delete
│   ├── Models/
│   │   ├── DashboardViewModel.cs      # Metric counts (Total, Open, Closed)
│   │   └── Ticket.cs                  # Client domain model with validation
│   ├── Services/
│   │   └── TicketService.cs           # Service layer consuming Web API via HttpClient
│   ├── Views/
│   │   ├── Shared/
│   │   │   └── _Layout.cshtml         # Minimalist monochrome layout
│   │   └── Ticket/
│   │       ├── Dashboard.cshtml       # Metrics overview cards
│   │       ├── Index.cshtml           # Ticket list with status filter
│   │       ├── Details.cshtml         # Full ticket details
│   │       ├── Create.cshtml          # Form to raise new ticket (Status = Open)
│   │       ├── Edit.cshtml            # Form to update priority & status
│   │       └── Delete.cshtml          # Delete confirmation view
│   ├── Program.cs
│   └── appsettings.json
│
├── HelpDesk.Tests/
│   └── Controllers/
│       └── TicketControllerTests.cs   # 13 xUnit unit tests mocking ITicketRepository with Moq
│
├── HelpDeskManagement.sln             # Visual Studio solution file
├── HelpDeskManagement.slnx            # Solution XML definition file
├── README.md                          # Solution documentation
└── .gitignore                         # Build ignore configuration
```

---

## ⚡ Solution Highlights & Architecture

1. **Web API Layer (`HelpDesk.Api`)**:
   - RESTful endpoints following standard HTTP verbs (`GET`, `POST`, `PUT`, `DELETE`).
   - Clean implementation of **Repository Pattern** (`ITicketRepository` and `TicketRepository`).
   - Uses EF Core with SQL Server (`SQLEXPRESS`).

2. **MVC Layer (`HelpDesk.Mvc`)**:
   - Implements **Service Layer (`TicketService`)** consuming Web API via `HttpClient`.
   - Controllers interact **strictly via the Service Layer** (zero direct database access).
   - **Dashboard**: Displays Total Tickets, Open Tickets, and Closed Tickets metric cards.
   - **Status Filtering**: Filter tickets by `Open`, `In Progress`, and `Closed`.
   - **Create Ticket**: Status is hardcoded to `Open`. Priority is selected via Dropdown.
   - **Edit Ticket**: Allows updating Title, Description, Priority (Dropdown), and Status (Dropdown).

3. **Unit Testing (`HelpDesk.Tests`)**:
   - Built with **xUnit** and **Moq**.
   - Tests `TicketController` actions by mocking `ITicketRepository`.
   - **Zero connection to SQL Server** during unit testing.
   - Passes all 13 unit tests.

---

## 🛠️ REST API Endpoints

| HTTP Method | API Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/api/Ticket/All` | Retrieve all tickets |
| **GET** | `/api/Ticket/{id}` | Get ticket details by ID |
| **POST** | `/api/Ticket` | Create a new support ticket |
| **PUT** | `/api/Ticket/{id}` | Update existing ticket |
| **DELETE** | `/api/Ticket/{id}` | Delete ticket by ID |
| **GET** | `/api/Ticket/Status/{status}` | Filter tickets by status |

---

## 🧪 Running Unit Tests

Run all xUnit unit tests using .NET CLI:
```bash
dotnet test HelpDesk.Tests/HelpDesk.Tests.csproj
```

---

## 🚀 Running the Projects Locally

1. **Start Web API**:
   ```bash
   dotnet run --project HelpDesk.Api/HelpDesk.Api.csproj --urls "http://localhost:5000"
   ```
2. **Start MVC Application**:
   ```bash
   dotnet run --project HelpDesk.Mvc/HelpDesk.Mvc.csproj --urls "http://localhost:5200"
   ```
3. Open `http://localhost:5200` in your browser.
