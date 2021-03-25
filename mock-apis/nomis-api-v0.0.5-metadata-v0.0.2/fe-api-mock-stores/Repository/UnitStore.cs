using System.Collections.Generic;
using System.Threading.Tasks;

using Microsoft.Extensions.Options;

using Nomis.Interfaces.Datasets.Models;
using Nomis.Interfaces.Datasets.Repository;
using Nomis.Interfaces.Core.Models;

using Nomis.MockStores.Models;

namespace Nomis.MockStores.Repository {
    public class UnitStore : IUnitStore {
        private Dictionary<string, List<Unit>> seeded;
        private readonly StoreConfiguration _config;

        public async Task<Unit> AddAsync(string datasetId, Unit unit) {
            await SeedDataAsync();

            var u = await GetAsync(datasetId, unit.Id);
            if(u == null) {
                seeded[datasetId].Add(unit);
                return unit;
            }
            else return u;
        }
        public async Task<Unit> UpdateAsync(string datasetId, Unit unit) {
            await SeedDataAsync();

            var u = await GetAsync(datasetId, unit.Id);
            if(u != null) {
                if(unit.Label != null) u.Label = unit.Label;
                return u;
            }
            else return null;
        }
        
        public async Task<bool> DeleteAsync(string datasetId, int unitId) {
            await SeedDataAsync();

            var unit = await GetAsync(datasetId, unitId);
            if(unit != null) return seeded[datasetId].Remove(unit);
            else return true; // Didn't exist anyway.
        }
        
        public async Task<Unit> GetAsync(string datasetId, int unitId) {
            await SeedDataAsync();

            var list = await GetAllAsync(datasetId, null);
            return list.Find(x => x.Id == unitId);
        }

        public async Task<List<Unit>> GetAllAsync(string datasetId, QueryFilterOptions options) {
            await SeedDataAsync();

            if(seeded.ContainsKey(datasetId)) return seeded[datasetId];
            else return new List<Unit>();
        }

        private async Task SeedDataAsync() {
            if(seeded != null) return; // Already initialised.
            else seeded = new Dictionary<string, List<Unit>>();

            // Only seed with test data if required by configuration.
            if(_config?.SeedTestData == false) return;

            seeded.Add("DC1101EW", GetCommonUnits());
            seeded.Add("DC1102EW", GetCommonUnits());
            seeded.Add("DC1104EW", GetCommonUnits());

            await Task.CompletedTask;
        }

        private List<Unit> GetCommonUnits() {
            return new List<Unit>() {
                new Unit() { Id = 0, Label = "Persons" },
                new Unit() { Id = 1, Label = "Households" }
            };
        }
        public UnitStore(IOptions<StoreConfiguration> options) {
            _config = options.Value;
        }
    }
}