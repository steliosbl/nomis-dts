using System.Threading.Tasks;
using System.Collections.Generic;

using Nomis.Interfaces.Metadata.Models;

namespace Nomis.Interfaces.Metadata.Repository {
    public interface IMetaRoleStore {
        Task<bool> AddAsync(MetaItemRole role);
        Task<bool> UpdateAsync(MetaItemRole role);
        Task<bool> DeleteAsync(string role);

        Task<IEnumerable<MetaItemRole>> GetAllAsync();
        Task<MetaItemRole> GetAsync(string role);

    }
}