using System.Collections.Generic;
using System.Threading.Tasks;

using Nomis.Interfaces.Datasets.Models;
using Nomis.Interfaces.Core.Models;

namespace Nomis.Interfaces.Datasets.Repository {
    public interface IDimensionStore {
        Task<Dimension> AddAsync(string datasetId, Dimension dimension);
        Task<Dimension> UpdateAsync(string datasetId, Dimension dimension);
        Task<bool> DeleteAsync(string datasetId, string name);
        
        Task<Dimension> GetAsync(string datasetId, string name);
        Task<List<Dimension>> GetAllAsync(string datasetId, QueryFilterOptions options);
    }
}