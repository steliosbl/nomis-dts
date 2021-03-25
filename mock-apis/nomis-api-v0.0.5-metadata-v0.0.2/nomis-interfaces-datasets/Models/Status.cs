using System;

namespace Nomis.Interfaces.Datasets.Models {
    public class Status {
        public int Id { get; set; }
        public string Symbol { get; set; }
        public string Message { get; set; }
        public Guid UUID { get; set; } = Guid.NewGuid();
        
        public Status() { }
    }
}