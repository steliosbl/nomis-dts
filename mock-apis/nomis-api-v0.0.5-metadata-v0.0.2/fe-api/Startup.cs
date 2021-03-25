using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Text.Json.Serialization;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.HttpsPolicy;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.OpenApi.Models;

using GraphiQl;
using GraphQL.Server;
using GraphQL.Types;

using fe_api.GraphQL;
using fe_api.GraphQL.Types;

using Nomis.Interfaces.Datasets.Repository;
using Nomis.Interfaces.Contacts.Repository;
using Nomis.Interfaces.Variables.Repository;
using Nomis.MockStores.Models;
using Nomis.MockStores.Repository;

namespace fe_api
{
    public class Startup
    {
        private string _apiVers = "0.0.5";
        private IWebHostEnvironment _env;

        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            services.Configure<StoreConfiguration>(Configuration.GetSection("MockStores"));

            services.AddControllers()
                .AddJsonOptions(options => 
                options.JsonSerializerOptions.Converters.Add(new JsonStringEnumConverter()));

            // Required for Swashbuckle
            services.AddMvcCore().AddApiExplorer();
            
            // Register the Swagger generator, defining 1 or more Swagger documents
            services.AddSwaggerGen(c =>
                {
                    c.SwaggerDoc($"v{_apiVers}", new OpenApiInfo
                    {
                        Version = $"v{_apiVers}",
                        Title = "Nomis API",
                        Description = "Nomis API providing public endpoints for discovery of datasets, variables and categories, and delivery of data. For administrative users, endpoints allow inspection of user accounts and dataset management.",
                        TermsOfService = new Uri("https://www.nomisweb.co.uk/terms"),
                        Contact = new OpenApiContact
                        {
                            Name = "Spencer Hedger",
                            Email = "support@nomisweb.co.uk",
                            Url = new Uri("https://www.nomisweb.co.uk"),
                        },
                        License = new OpenApiLicense
                        {
                            Name = "Use under MIT",
                            Url = new Uri("https://example.com/license"),
                        }
                    });

                    // Set the comments path for the Swagger JSON and UI.
                    var xmlFile = $"{System.Reflection.Assembly.GetExecutingAssembly().GetName().Name}.xml";
                    var xmlPath = System.IO.Path.Combine(AppContext.BaseDirectory, xmlFile);
                    c.IncludeXmlComments(xmlPath);
                });

            // Set up the data stores for dependency injection.
            services.AddSingleton<IDatasetStore, DatasetStore>();
            services.AddSingleton<IContactStore, ContactStore>();
            services.AddSingleton<IDimensionStore, DimensionStore>();
            services.AddSingleton<IVariableStore, VariableStore>();
            services.AddSingleton<ICategoryStore, CategoryStore>();
            services.AddSingleton<ICategoryTypeStore, CategoryTypeStore>();
            services.AddSingleton<IObservationStore, ObservationStore>();
            services.AddSingleton<IStatusStore, StatusStore>();
            services.AddSingleton<IUnitStore, UnitStore>();

            // GraphQL
            services.AddScoped<NomisQuery>();
            services.AddScoped<ContactType>();
            services.AddScoped<ISchema, NomisSchema>();
            services.AddGraphQL(options => {
                options.EnableMetrics = false; //_env.IsDevelopment();
                options.UnhandledExceptionDelegate = ctx => { Console.WriteLine(ctx.OriginalException); };
            })
                .AddSystemTextJson(deserializerSettings => { }, serializerSettings => { })
                .AddGraphTypes(ServiceLifetime.Scoped);
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
        {
            _env = env;

            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }

            // Initial basic CORS setup.
            app.UseCors(options => {
                    options.AllowAnyOrigin();
                    options.AllowAnyMethod();
                    options.AllowAnyHeader();
                }
            );

            // Enable middleware to serve generated Swagger as a JSON endpoint.
            app.UseSwagger();

            // Enable middleware to serve swagger-ui (HTML, JS, CSS, etc.),
            // specifying the Swagger JSON endpoint.
            app.UseSwaggerUI(c =>
            {
                c.SwaggerEndpoint($"/swagger/v{_apiVers}/swagger.json", $"Nomis API V{_apiVers}");
            });

            // GraphQL
            app.UseGraphiQl("/graphql");
            app.UseGraphQL<ISchema>();

            app.UseHttpsRedirection();

            app.UseRouting();

            app.UseAuthorization();

            app.UseEndpoints(endpoints =>
            {
                endpoints.MapControllers();
            });
        }
    }
}
