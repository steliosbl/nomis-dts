using System.Collections.Generic;
using System.Threading.Tasks;

using Microsoft.Extensions.Options;

using Nomis.Interfaces.Datasets.Models;
using Nomis.Interfaces.Datasets.Repository;
using Nomis.Interfaces.Core.Models;

using Nomis.MockStores.Models;

namespace Nomis.MockStores.Repository {
    public class DimensionStore : IDimensionStore {
        private Dictionary<string, List<Dimension>> seeded;
        private readonly StoreConfiguration _config;

        public async Task<Dimension> AddAsync(string datasetId, Dimension dimension) {
            await SeedDataAsync();

            if(!seeded.ContainsKey(datasetId)) seeded.Add(datasetId, new List<Dimension>() { dimension });
            else seeded[datasetId].Add(dimension);
            
            return dimension;
        }
        public async Task<Dimension> UpdateAsync(string datasetId, Dimension dimension) {
            await SeedDataAsync();

            Dimension d = await GetAsync(datasetId, dimension.Name);

            if(dimension.Label != null) d.Label = dimension.Label;

            return d;
        }
        public async Task<bool> DeleteAsync(string datasetId, string name) {
            await SeedDataAsync();

            Dimension d = await GetAsync(datasetId, name);

            if(d != null) return seeded[datasetId].Remove(d);
            else return true; // Didn't exist anyway.
        }
        
        public async Task<Dimension> GetAsync(string datasetId, string name) {
            await SeedDataAsync();
            
            List<Dimension> dimensions = await GetAllAsync(datasetId, null);
            return dimensions?.Find(d => d.Name == name);
        }
        public async Task<List<Dimension>> GetAllAsync(string datasetId, QueryFilterOptions options) {
            await SeedDataAsync();

            if(seeded.ContainsKey(datasetId)) return seeded[datasetId];
            else return null;
        }

        private async Task SeedDataAsync() {
            if(seeded != null) return; // Already initialised.
            else seeded = new Dictionary<string, List<Dimension>>();

            // Only seed with test data if required by configuration.
            if(_config?.SeedTestData == false) return;

            seeded.Add(
                "DC1101EW",
                new List<Dimension>() {
                    new Dimension() {
                        Name = "geography",
                        Label = "Geography",
                        Variable = new VariableMapping() { Name = "GEOGRAPHY", View = "census" },
                        Database = new DatabaseInfo() { IsKey = true, Index = 0 }
                    },
                    new Dimension() {
                        Name = "age",
                        Label = "Age",
                        Variable = new VariableMapping() { Name = "AGE_7", View = "census" },
                        Database = new DatabaseInfo() { IsKey = false, Index = 1 }
                    },
                    new Dimension() {
                        Name = "mar_stat",
                        Label = "Marital Status",
                        Variable = new VariableMapping() { Name = "MARSTAT_6", View = "census" },
                        Database = new DatabaseInfo() { IsKey = false, Index = 2 }
                    },
                    new Dimension() {
                        Name = "sex",
                        Label = "Sex",
                        Variable = new VariableMapping() { Name = "SEX", View = "census" },
                        Database = new DatabaseInfo() { IsKey = false, Index = 3 }
                    }
                }
            );

            seeded.Add(
                "DC1102EW",
                new List<Dimension>() {
                    new Dimension() {
                        Name = "geography",
                        Label = "Geography",
                        Variable = new VariableMapping() { Name = "GEOGRAPHY", View = "census" },
                        Database = new DatabaseInfo() { IsKey = true, Index = 0 }
                    },
                    new Dimension() {
                        Name = "age",
                        Label = "Age",
                        Variable = new VariableMapping() { Name = "AGE_7", View = "census" },
                        Database = new DatabaseInfo() { IsKey = false, Index = 1 }
                    },
                    new Dimension() {
                        Name = "living_arr",
                        Label = "Living arrangements",
                        Variable = new VariableMapping() { Name = "LIV_ARR", View = "census" },
                        Database = new DatabaseInfo() { IsKey = false, Index = 2 }
                    },
                    new Dimension() {
                        Name = "sex",
                        Label = "Sex",
                        Variable = new VariableMapping() { Name = "SEX", View = "census" },
                        Database = new DatabaseInfo() { IsKey = false, Index = 3 }
                    }
                }
            );

            seeded.Add(
                "DC1104EW",
                new List<Dimension>() {
                    new Dimension() {
                        Name = "geography",
                        Label = "Geography",
                        Variable = new VariableMapping() { Name = "GEOGRAPHY", View = "census" },
                        Database = new DatabaseInfo() { IsKey = true, Index = 0 }
                    },
                    new Dimension() {
                        Name = "sex",
                        Label = "Sex",
                        Variable = new VariableMapping() { Name = "SEX", View = "census" },
                        Database = new DatabaseInfo() { IsKey = false, Index = 1 }
                    },
                    new Dimension() {
                        Name = "age",
                        Label = "Age",
                        Variable = new VariableMapping() { Name = "AGE_7", View = "census" },
                        Database = new DatabaseInfo() { IsKey = false, Index = 2 }
                    }
                }
            );

            await Task.CompletedTask;
        }

        public DimensionStore(IOptions<StoreConfiguration> options) {
            _config = options.Value;
        }
    }
}