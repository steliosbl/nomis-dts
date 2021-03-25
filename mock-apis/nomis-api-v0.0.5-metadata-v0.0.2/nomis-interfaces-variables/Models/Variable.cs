using System;
using System.Collections.Generic;
namespace Nomis.Interfaces.Variables.Models {
    public class Variable {
        public string Name { get; set; }
        public string Label { get; set; }
        public Guid UUID { get; set; } = Guid.NewGuid();

        public List<string> Defaults { get; set; }
    }
}