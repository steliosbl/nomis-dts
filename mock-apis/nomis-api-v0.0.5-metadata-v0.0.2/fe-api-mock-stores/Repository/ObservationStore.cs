using System;
using System.Collections.Generic;
using System.Threading.Tasks;

using Microsoft.Extensions.Options;

using Nomis.Interfaces.Datasets.Models;
using Nomis.Interfaces.Datasets.Repository;
using Nomis.Interfaces.Variables.Repository;
using Nomis.Interfaces.Core.Models;

using Nomis.MockStores.Models;

namespace Nomis.MockStores.Repository {
    public class ObservationStore : IObservationStore {
        private readonly IDatasetStore _datasetStore;
        private readonly IDimensionStore _dimensionStore;
        private readonly ICategoryStore _categoryStore;
        private readonly StoreConfiguration _config;

        private Dictionary<string, List<ObservationRecord>> seeded;

        public async Task<RowMajorObservations> AddAsync(string datasetId, RowMajorObservations observations) {
            await SeedDataAsync();

            var dimensions = await _dimensionStore.GetAllAsync(datasetId, null);
            if(dimensions == null) throw new System.ArgumentException("Unknown dataset ID or dataset has no dimensions defined.");

            for(int i = 0; i < observations.Values.Count; i++) {
                var rec = CreateRecord(dimensions, observations.GetCodes(i), i, observations);

                // Only check the dimensions on the first observation, because all are same shape.
                await AddAsync(datasetId, rec, i == 0);
            }

            return observations;
        }

        private async Task<ObservationRecord> AddAsync(string datasetId, ObservationRecord observation, bool checkDimensions) {
            await SeedDataAsync();

            // Ensure that the incoming observation has dimensions that match the dataset dimension definition.
            if(checkDimensions) {
                var dimensions = await _dimensionStore.GetAllAsync(datasetId, null);
                if(dimensions == null) throw new System.ArgumentException("Unknown dataset ID or dataset has no dimensions defined.");

                // For each of the dimensions, make sure that there is a matching dimension in the incoming observation.
                bool failDimensionCheck = false;
                if(observation.Dimensions != null) {
                    foreach(var d in dimensions) {
                        if(observation.Dimensions.Find(x => x.Name == d.Name) == null) failDimensionCheck = true; 
                    }
                }
                else failDimensionCheck = true;

                // Basic check on observation object.
                if( failDimensionCheck || observation.Observation == null) throw new System.FormatException("Observation record not valid for this dataset.");
            }

            // Check dataset is already in seeded data.
            if(seeded.ContainsKey(datasetId)) {
                // See if value already exists.
                var obs = await GetObservationRecordAsync(datasetId, observation.Dimensions);

                // If it exists update the value.
                if(obs != null) {
                    obs.Observation = observation.Observation;
                }
                else seeded[datasetId].Add(observation); // Otherwise add the new observation.
            }
            else seeded.Add(datasetId, new List<ObservationRecord>() { observation }); // Dataset didn't exist in seeded data.

            return observation;
        }

        public async Task<bool> DeleteAsync(string datasetId) {
            await SeedDataAsync();

            if(seeded.ContainsKey(datasetId)) {
                seeded[datasetId].Clear();
                return true;
            }
            else return true; // Didn't exist anyway.
        }

        private async Task<ObservationRecord> GetObservationRecordAsync(string datasetId, ICollection<DimensionMapping> dimensions) {
            await SeedDataAsync();

            var obs = await GetObservationsEnumerableAsync(datasetId, null);

            foreach(var o in obs) {
                // Check each of the dimensions matches.
                bool matches = true;

                foreach(var d in dimensions) {
                    if(o.Dimensions.Find(x => x.Name == d.Name && x.Code == d.Code) == null) {
                        matches = false;
                        break;
                    }
                }

                if(matches) return o;
            }

            return null;
        }

        public async Task<RowMajorObservations> GetAllAsync(string datasetId, QueryFilterOptions options = null) {
            await SeedDataAsync();

            var obs = await GetObservationsEnumerableAsync(datasetId, options);

            List<string> ids = new List<string>();
            List<List<string>> dimensions = new List<List<string>>();
            List<double> values = new List<double>();
            List<int> status = new List<int>();

            foreach(var o in obs) {
                // Add the codes for the dimensions (where not present).
                for(int i = 0; i < o.Dimensions.Count; i++) {
                    var mapping = o.Dimensions[i];

                    // Dimension name.
                    if(!ids.Contains(mapping.Name)) ids.Add(mapping.Name);

                    List<string> codes;
                    
                    if(dimensions.Count > i) codes = dimensions[i];
                    else {
                        codes = new List<string>();
                        dimensions.Add(codes);
                    }

                    // Add the code if not present.
                    if(!codes.Contains(mapping.Code)) codes.Add(mapping.Code);
                }

                values.Add(o.Observation.Value);
                status.Add(o.Observation.StatusId);
            }

            return new RowMajorObservations() {
                Dataset = datasetId,
                Dimensions = ids,
                Codes = dimensions,
                Values = values,
                Statuses = status
            };
        }

        private async Task<IEnumerable<ObservationRecord>> GetObservationsEnumerableAsync(string datasetId, QueryFilterOptions options) {
            await SeedDataAsync();

            // List to store observations.
            if(!seeded.ContainsKey(datasetId)) {
                seeded.Add(datasetId, new List<ObservationRecord>(1000));
                return seeded[datasetId];
            }
            else {
                // Bodge in a basic filter.
                if(options != null && !String.IsNullOrEmpty(options.Query.Value)) {
                    string[] opts = options.Query.Value.Split(" and ");
                    var obs = seeded[datasetId];

                    foreach(string s in opts) {
                        string[] term = s.Split(":");  // Should have s="geography:E12000001"

                        obs = obs.FindAll(d => {
                            return (d.Dimensions.Find(o => o.Name == term[0].Trim() && o.Code == term[1].Trim()) != null);
                        });
                    }

                    return obs;
                }
                else return seeded[datasetId];
            }
        }

        private async Task SeedDataAsync() {
            if(seeded != null) return;
            else seeded = new Dictionary<string, List<ObservationRecord>>();

            // Only seed with test data if required by configuration.
            if(_config?.SeedTestData == false) return;

            // Loop over datasets.
            var datasets = await _datasetStore.GetAllAsync(null);
            datasets.ForEach(async d => {
                var obs = new List<ObservationRecord>();

                var dimensions = await _dimensionStore.GetAllAsync(d.Id, null);

                if(dimensions == null) return;

                List<List<DimensionMapping>> m = new List<List<DimensionMapping>>();

                // Loop over dimensions to create permutations.
                dimensions.ForEach(async dim => {
                    var mappings = new List<DimensionMapping>();
                    m.Add(mappings);

                    var categories = await _categoryStore.GetAllAsync(dim.Variable.Name, dim.Variable.View, null);

                    // Loop over categories.
                    categories.ForEach(cat => {
                        mappings.Add(new DimensionMapping() { Name = dim.Name, Code = cat.Code });
                    });
                });

                GeneratePermutations(m, obs, 0, new List<DimensionMapping>(), new Random());
                seeded.Add(d.Id, obs);
            });
        }

        private void GeneratePermutations(List<List<DimensionMapping>> lists, List<ObservationRecord> result, int depth, List<DimensionMapping> current, Random rand) {
            if (depth == lists.Count) {
                List<DimensionMapping> complete = new List<DimensionMapping>();

                // Clone out current state.
                current.ForEach(e => {
                    complete.Add(new DimensionMapping() {
                        Name = e.Name,
                        Code = e.Code
                    });
                });

                result.Add(new ObservationRecord() {
                    Dimensions = complete,
                    Observation = new ObservationValue() {
                        Value = rand.Next(10, 100000),
                        StatusId = 0
                    }
                });

                return;
            }

            List<DimensionMapping> m = lists[depth];

            for (int i = 0; i < m.Count; i++) {
                // Swap out dimension 
                DimensionMapping map = current.Find(d => d.Name == m[i].Name);
                if(map == null) current.Add(new DimensionMapping() { Name = m[i].Name, Code = m[i].Code }); // New entry.
                else map.Code = m[i].Code; // Update existing.

                GeneratePermutations(lists, result, depth + 1, current, rand);
            }
        }

        public ObservationRecord CreateRecord(List<Dimension> dimensions, List<string> codes, int index, RowMajorObservations observations) {
            if(codes.Count != dimensions.Count) return null;

            ObservationRecord rec = new ObservationRecord() {
                Dimensions = new List<DimensionMapping>(),
                Observation = new ObservationValue()
            };

            for(int i = 0; i < codes.Count; i++) {
                rec.Dimensions.Add(new DimensionMapping() { Name = dimensions[i].Name, Code = codes[i]});
            }

            // Where is the data stored in the row major order array.
            rec.Observation.Value = observations.Values[index];
            if(observations.Statuses != null) rec.Observation.StatusId = observations.Statuses[index];

            return rec;
        }

        public ObservationStore(
            IDatasetStore datasetStore,
            IDimensionStore dimensionStore,
            ICategoryStore categoryStore,
            IOptions<StoreConfiguration> options)
        {
            _datasetStore = datasetStore;
            _dimensionStore = dimensionStore;
            _categoryStore = categoryStore;
            _config = options.Value;
        }
    }
}