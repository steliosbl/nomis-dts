using System.Collections.Generic;
using System.Threading.Tasks;

using Nomis.Interfaces.Datasets.Models;
using Nomis.Interfaces.Core.Models;

namespace Nomis.Interfaces.Datasets.Repository {
    public interface IStatusStore {
        Task<Status> AddAsync(string datasetId, Status status);
        Task<Status> UpdateAsync(string datasetId, Status status);
        Task<bool> DeleteAsync(string datasetId, int flagId);
        
        Task<Status> GetAsync(string datasetId, int statusId);
        Task<List<Status>> GetAllAsync(string datasetId, QueryFilterOptions options);
    }
}