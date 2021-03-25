using System;
using System.Collections.Generic;

namespace Nomis.Interfaces.Datasets.Models {
    public enum DimensionRole { Temporal, Spatial, Measures, Normal }

    public class Dimension {
        public string Name { get; set; }

        // Optionally override label defined for the underlying variable.
        public string Label { get; set; }
        public bool IsAdditive { get; set; } = true;
        public VariableMapping Variable { get; set; }
        public DimensionRole Role { get; set; } = DimensionRole.Normal;
        public bool CanFilter { get; set; } = true;
        public List<string> Defaults { get; set; }
        public DatabaseInfo Database { get; set; }
        public Guid UUID { get; set; } = Guid.NewGuid();

        public Dimension() { }
    }
}