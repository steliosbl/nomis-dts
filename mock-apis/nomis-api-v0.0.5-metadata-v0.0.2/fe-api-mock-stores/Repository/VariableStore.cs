using System;
using System.IO;
using System.Collections.Generic;
using System.Threading.Tasks;

using Microsoft.Extensions.Options;

using Nomis.Interfaces.Variables.Models;
using Nomis.Interfaces.Variables.Repository;
using Nomis.Interfaces.Core.Models;

using Nomis.MockStores.Models;

namespace Nomis.MockStores.Repository {
    public class VariableStore : IVariableStore {
        private List<Variable> seeded;
        private readonly StoreConfiguration _config;

        public async Task<Variable> AddAsync(Variable variable) {
            await SeedDataAsync();

            if(seeded.Find(v => v.Name == variable.Name) != null) return null;
            else {
                seeded.Add(variable);
                return variable;
            }
        }

        public async Task<Variable> UpdateAsync(Variable variable) {
            await SeedDataAsync();

            Variable v = await GetAsync(variable.Name, null);
            if(v != null) {
                if(variable.Name != null) v.Name = variable.Name;
            }

            return v;
        }

        public async Task<bool> DeleteAsync(string id) {
            await SeedDataAsync();

            Variable v = await GetAsync(id);
            
            if(v != null) return seeded.Remove(v);
            else return true; // Didn't exist anyway.
        }
        
        public async Task<Variable> GetAsync(string id, string view = null) {
            await SeedDataAsync();

            return seeded.Find(v => v.Name == id);
        }
        public async Task<List<Variable>> GetAllAsync(QueryFilterOptions options = null) {
            await SeedDataAsync();

            return seeded;
        }

        private async Task SeedDataAsync() {
            if(seeded != null) return;
            else seeded = new List<Variable>();

            // Only seed with test data if required by configuration.
            if(_config?.SeedTestData == false) return;

            seeded.Add(new Variable() {
                Name = "GEOGRAPHY",
                Label = "Geographic area"
            });
            seeded.Add(new Variable() {
                Name = "MARSTAT_6",
                Label = "Marital status"
            });
            seeded.Add(new Variable() {
                Name = "AGE_7",
                Label = "Age"
            });
            seeded.Add(new Variable() {
                Name = "LIV_ARR",
                Label = "Living arrangements"
            });
            seeded.Add(new Variable() {
                Name = "SEX",
                Label = "Sex"
            });

            await Task.CompletedTask;
        }

        public VariableStore(IOptions<StoreConfiguration> options) {
            _config = options.Value;
        }
    }
}