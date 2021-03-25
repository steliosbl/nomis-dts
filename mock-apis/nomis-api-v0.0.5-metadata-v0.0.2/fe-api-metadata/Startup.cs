using System;

using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.OpenApi.Models;

using Nomis.Interfaces.Metadata.Repository;
using Nomis.Api.Metadata.Models.Store;

namespace Nomis.Api.Metadata
{
    public class Startup
    {
        private string _apiVers = "0.0.2";

        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            services.Configure<InMemoryStoreConfiguration>(Configuration.GetSection("InMemoryStores"));

            services.AddControllers();

            // Required for Swashbuckle
            services.AddMvcCore().AddApiExplorer();
            
            // Register the Swagger generator, defining 1 or more Swagger documents
            services.AddSwaggerGen(c =>
                {
                    c.SwaggerDoc($"v{_apiVers}", new OpenApiInfo
                    {
                        Version = $"v{_apiVers}",
                        Title = "Metadata API",
                        Description = "API providing metadata storage and management.",
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

            services.AddSingleton<IMetadataStore, MetadataDbStoreInMemory>();
            services.AddSingleton<IRdfNamespaceStore, RdfNamespaceDbStoreInMemory>();
            services.AddSingleton<IMetaRoleStore, MetaRoleDbStoreInMemory>();
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }

            // Enable middleware to serve generated Swagger as a JSON endpoint.
            app.UseSwagger();

            // Enable middleware to serve swagger-ui (HTML, JS, CSS, etc.),
            // specifying the Swagger JSON endpoint.
            app.UseSwaggerUI(c =>
            {
                c.SwaggerEndpoint($"/swagger/v{_apiVers}/swagger.json", $"Nomis API V{_apiVers}");
            });

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
