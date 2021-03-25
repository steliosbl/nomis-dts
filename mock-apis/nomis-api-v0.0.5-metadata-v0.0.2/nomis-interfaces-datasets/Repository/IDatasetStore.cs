using System.Collections.Generic;
using System.Threading.Tasks;

using Nomis.Interfaces.Datasets.Models;
using Nomis.Interfaces.Core.Models;

namespace Nomis.Interfaces.Datasets.Repository {
    public interface IDatasetStore {
        Task<Dataset> AddAsync(Dataset dataset);
        Task<Dataset> UpdateAsync(Dataset dataset);
        Task<bool> DeleteAsync(string id);
        
        Task<Dataset> GetAsync(string id);
        Task<List<Dataset>> GetAllAsync(QueryFilterOptions options);
    }
}