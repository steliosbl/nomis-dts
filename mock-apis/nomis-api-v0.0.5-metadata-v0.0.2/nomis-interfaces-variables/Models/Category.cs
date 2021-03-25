using System;
using System.Collections.Generic;

namespace Nomis.Interfaces.Variables.Models {
    public class Category {
        public string Code { get; set; }
        public string Title { get; set; }
        public int Keyval { get; set; }
        public string TypeId { get; set; }
        public Guid UUID { get; set; } = Guid.NewGuid();

        public List<CategoryAncestor> Ancestors{ get; set; }
    }
}