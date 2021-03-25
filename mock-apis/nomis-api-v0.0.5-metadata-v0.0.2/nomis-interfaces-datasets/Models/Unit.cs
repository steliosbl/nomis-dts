using System;

namespace Nomis.Interfaces.Datasets.Models {
    public class Unit {
        public int Id { get; set; }
        public int Decimals { get; set; }
        public string Label { get; set; }
        public string Symbol { get; set; }
        public string Position { get; set; }
        public Guid UUID { get; set; } = Guid.NewGuid();
        
        public Unit() { }
    }
}