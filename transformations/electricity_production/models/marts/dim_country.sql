with final as (

    select
      name,
      cca2_identifier,
      ccn3_identifier,
      is_independent,
      is_landlocked,
      is_un_member,
      capital_city,
      region,
      subregion,
      latitude,
      longitude,
      area_sq_km,
      population,
      flag,
      google_maps_link,
      continent,
      subcontinent,
      start_of_week
    from {{ ref('stg_rest_countries') }}

)

select * from final