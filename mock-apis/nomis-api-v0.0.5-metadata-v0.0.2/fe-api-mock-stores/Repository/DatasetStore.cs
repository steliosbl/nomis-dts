using System.Collections.Generic;
using System.Threading.Tasks;

using Microsoft.Extensions.Options;

using Nomis.Interfaces.Datasets.Models;
using Nomis.Interfaces.Datasets.Repository;
using Nomis.Interfaces.Core.Models;

using Nomis.MockStores.Models;

namespace Nomis.MockStores.Repository {
    public class DatasetStore : IDatasetStore {
        private List<Dataset> seeded;
        private readonly StoreConfiguration _config;

        public async Task<Dataset> AddAsync(Dataset dataset) {
            await SeedDataAsync();
            
            if(seeded.Find(d => d.Id == dataset.Id) != null) return null;
            else seeded.Add(dataset);

            return dataset;
        }

        public async Task<Dataset> UpdateAsync(Dataset dataset) {
            await SeedDataAsync();

            Dataset d = await GetAsync(dataset.Id);

            if(d != null) {
                if(dataset.ContactId != null) d.ContactId = dataset.ContactId;
                if(dataset.Title != null) d.Title = dataset.Title;

                return d;
            }
            else return null;
        }

        public async Task<bool> DeleteAsync(string id) {
            await SeedDataAsync();

            Dataset d = await GetAsync(id);
            if(d != null) return seeded.Remove(d);
            else return true; // Didn't exist anyway.
        }
        
        public async Task<Dataset> GetAsync(string id) {
            await SeedDataAsync();

            return seeded.Find(d => d.Id == id);
        }

        public async Task<List<Dataset>> GetAllAsync(QueryFilterOptions options = null) {
            await SeedDataAsync();
            return Filter(seeded, options);
        }

        private List<Dataset> Filter(List<Dataset> list, QueryFilterOptions q) {
            if(q == null || q.Query == null || string.IsNullOrEmpty(q.Query.Value)) return seeded;
            else return seeded.FindAll(d => {
                return d.Title.Contains(q.Query.Value.Replace("title=", ""), System.StringComparison.InvariantCultureIgnoreCase);
            });
        }

        private async Task SeedDataAsync() {
            if(seeded != null) return;
            else seeded = new List<Dataset>();

            // Only seed with test data if required by configuration.
            if(_config?.SeedTestData == false) return;

            seeded.Add(new Dataset() {
                Id = "DC1101EW",
                Title = "Marital and civil partnership status by sex by age - Household Reference Persons",
                ContactId = "census"
            });
            seeded.Add(new Dataset() {
                Id = "DC1102EW",
                Title = "Living arrangements by sex by age - Household Reference Persons",
                ContactId = "census"
            });
            seeded.Add(new Dataset() {
                Id = "DC1104EW",
                Title = "Residence type by sex by age",
                ContactId = "census"
            });

            await Task.CompletedTask;
        }

        public DatasetStore(IOptions<StoreConfiguration> options) {
            _config = options.Value;
        }
    }
}