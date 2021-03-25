using System.Collections.Generic;

namespace Nomis.Interfaces.Variables.Models {
    public class CategoryAncestor {
        public string Code { get; set; }
        public List<string> Hierarchies { get; set; }
    }
}