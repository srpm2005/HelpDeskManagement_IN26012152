using HelpDesk.Api.Data;
using HelpDesk.Api.Repositories;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// API Controller configuration
builder.Services.AddControllers();

// SQL Server Database Context configuration
builder.Services.AddDbContext<HelpDeskDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

// Repository dependency registration
builder.Services.AddScoped<ITicketRepository, TicketRepository>();

// Enable CORS for client applications
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll", policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyMethod()
              .AllowAnyHeader();
    });
});

builder.Services.AddOpenApi();

var app = builder.Build();

// Ensure local database schema and initial seed data are populated
using (var scope = app.Services.CreateScope())
{
    var dbContext = scope.ServiceProvider.GetRequiredService<HelpDeskDbContext>();
    dbContext.Database.EnsureCreated();
}

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

app.UseCors("AllowAll");
app.UseAuthorization();
app.MapControllers();

app.Run();
