using GraphQL.Types;

using Nomis.Interfaces.Datasets.Models;

public class DimensionRoleType : EnumerationGraphType<DimensionRole>
{
    public DimensionRoleType()
    {
        Name = "DimensionRoleType";
    }
}