with base_data as (

    select
        name,
        tld,
        cca2,
        ccn3,
        independent,
        status,
        un_member,
        currencies,
        idd,
        capital,
        alt_spellings,
        region,
        languages,
        translations,
        latlng,
        landlocked,
        area,
        demonyms,
        flag,
        maps,
        population,
        car,
        timezones,
        continents,
        flags,
        coat_of_arms,
        start_of_week,
        capital_info,
        cioc,
        subregion,
        fifa,
        borders,
        gini,
        postal_code
    from {{ source('electricity', 'countries') }}

),

final as (

    select
        name ->> '$.common' as name,
        cca2 as cca2_identifier,
        ccn3 as ccn3_identifier,
        independent::boolean as is_independent,
        landlocked::boolean as is_landlocked,
        un_member as is_un_member,
        capital ->> 0 as capital_city,
        region,
        subregion,
        cast(latlng ->> 0 as decimal(8,6)) as latitude,
        cast(latlng ->> 1 as decimal(9,6)) as longitude,
        area as area_sq_km,
        population::int as population,
        flag,
        maps ->> '$.googleMaps' as google_maps_link,
        continents ->> 0 as continent,
        continents ->> 1 as subcontinent,
        upper(left(start_of_week, 1)) || lower(substring(start_of_week, 2, strlen(start_of_week))) as start_of_week
    from base_data
)

select * from final