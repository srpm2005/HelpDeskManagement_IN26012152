using HelpDesk.Mvc.Services;

var builder = WebApplication.CreateBuilder(args);

// Register MVC views and controllers
builder.Services.AddControllersWithViews();

// Service Layer registration with HttpClient for Web API communication
var apiBaseUrl = builder.Configuration["ApiSettings:BaseUrl"] ?? "http://localhost:5000/";
builder.Services.AddHttpClient<TicketService>(client =>
{
    client.BaseAddress = new Uri(apiBaseUrl);
});

var app = builder.Build();

if (!app.Environment.IsDevelopment())
{
    app.UseDeveloperExceptionPage();
}

app.UseStaticFiles();
app.UseRouting();
app.UseAuthorization();

// Default route configuration pointing to Ticket Dashboard
app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Ticket}/{action=Dashboard}/{id?}");

app.Run();
