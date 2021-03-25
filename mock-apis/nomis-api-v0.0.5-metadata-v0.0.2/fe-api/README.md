# Nomis datasets and variables API
This is the frontend for the Nomis API, it provides access to `/contacts`, `/datasets` and `/variables` endpoints.

## GraphQL
A Graph*i*QL endpoint is exposed at `/graphql`.

## Documentation
Full OAS 3.0 browsable documentation is available at `/swagger`.

## Configuration
The in-memory mock stores (`fe-api-mock-stores`) accept the following configuration,
which can be placed in the `appsettings.json` file:

```
"MockStores": {
    "SeedTestData": false
}
```

When `SeedTestData` is `true`, some simple test datasets and observations are added. Depending upon call order,
the seeding may populate a new dataset with sample observations, so in testing data loading, it is important
to have this property set to `false`.

## Dependencies

### NuGet packages
- `Swashbuckle.AspNetCore`
- `graphiql`

### Core dependencies
The following repositories are required:

- https://github.com/nomisweb/nomis-interfaces-datasets
- https://github.com/nomisweb/nomis-interfaces-contacts
- https://github.com/nomisweb/nomis-interfaces-variables

### Additional dependencies
The following store implementations are used as appropriate:

- https://github.com/nomisweb/fe-api-mock-stores (in-memory stores for demonstration purposes)
- https://github.com/nomisweb/nomis-legacy-datasets (implementation for legacy backend systems)
- https://github.com/nomisweb/nomis-legacy-contacts (implementation for legacy backend systems)
- https://github.com/nomisweb/nomis-legacy-variables (implementation for legacy backend systems)