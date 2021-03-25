namespace Nomis.Interfaces.Core.Models {
    // Represents the syntax used when parsing a particular parameter
    public enum Syntax { Lucene };

    public class FilterValue<T> {
        // Value of the filter (the term or condition typed).
        public T Value { get; set; }
        // Determines how the syntax of the query should be interpreted.
        public Syntax Syntax { get; set; } = Syntax.Lucene;
    }

    // Group various filter options together, rather than passing
    // them as individual parameters to data store methods.
    public class QueryFilterOptions {
        // Query is often passed as "q=" on an API endpoint. It represents
        // the constraints to which the returned result set should meet.
        public FilterValue<string> Query { get; set; } = new FilterValue<string>();

        // Sort requirements.
        public string Sort { get; set; }

        public QueryFilterOptions() { }
    }
}