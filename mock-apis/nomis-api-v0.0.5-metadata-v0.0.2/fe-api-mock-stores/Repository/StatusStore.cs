using System.Collections.Generic;
using System.Threading.Tasks;

using Microsoft.Extensions.Options;

using Nomis.Interfaces.Datasets.Models;
using Nomis.Interfaces.Datasets.Repository;
using Nomis.Interfaces.Core.Models;

using Nomis.MockStores.Models;

namespace Nomis.MockStores.Repository {
    public class StatusStore : IStatusStore {
        private Dictionary<string, List<Status>> seeded;
        private readonly StoreConfiguration _config;

        public async Task<Status> AddAsync(string datasetId, Status status) {
            await SeedDataAsync();

            if(!seeded.ContainsKey(datasetId)) seeded.Add(datasetId, new List<Status>() { status });
            else seeded[datasetId].Add(status);

            return status;
        }

        public async Task<Status> UpdateAsync(string datasetId, Status status) {
            await SeedDataAsync();

            Status f = await GetAsync(datasetId, status.Id);

            if(status.Message != null) f.Message = status.Message;
            if(status.Symbol != null) f.Symbol = status.Symbol;

            return f;
        }
        public async Task<bool> DeleteAsync(string datasetId, int statusId) {
            await SeedDataAsync();

            List<Status> status = await GetAllAsync(datasetId, null);
            Status s = await GetAsync(datasetId, statusId);

            if(s != null) return status.Remove(s);
            else return true; // Didn't exist anyway.
        }
        
        public async Task<Status> GetAsync(string datasetId, int statusId) {
            await SeedDataAsync();

            List<Status> status = await GetAllAsync(datasetId, null);

            if(status != null) return status.Find(f => f.Id == statusId);
            else return null;
        }
        public async Task<List<Status>> GetAllAsync(string datasetId, QueryFilterOptions options) {
            await SeedDataAsync();
            
            if(seeded.ContainsKey(datasetId)) return seeded[datasetId];
            else return null;
        }

        private async Task SeedDataAsync() {
            if(seeded != null) return; // Already initialised.
            else seeded = new Dictionary<string, List<Status>>();

            // Only seed with test data if required by configuration.
            if(_config?.SeedTestData == false) return;

            seeded.Add("DC1101EW", GetCommonStatus());
            seeded.Add("DC1102EW", GetCommonStatus());
            seeded.Add("DC1104EW", GetCommonStatus());

            await Task.CompletedTask;
        }

        private List<Status> GetCommonStatus() {
            List<Status> common = new List<Status>();

            common.Add(new Status() {
                Id = 0,
                Symbol = "A",
                Message = "Normal value."
            });

            common.Add(new Status() {
                Id = 1,
                Symbol = "-",
                Message = "Missing value."
            });

            return common;
        }

        public StatusStore(IOptions<StoreConfiguration> options) {
            _config = options.Value;
        }
    }
}