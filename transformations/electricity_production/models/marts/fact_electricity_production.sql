with base_data as (

    select
      country,
      year,
      month,
      product,
      production_gwh
    from {{ ref('stg_iea_electricity_production') }}
    where product <> 'Not specified'
    and country not like 'OECD%'
    and country <> 'IEA Total'

),

countries_mapping as (

    select
      country_name,
      country_alias
    from {{ ref('countries_mapping') }}
),

final as (

    select
      {{ dbt_utils.generate_surrogate_key(['base.country', 'base.year', 'base.month', 'base.product']) }} as unique_id,
      coalesce(countries.country_alias, base.country) as country,
      make_date(base.year, base.month, 1) as production_month,
      base.product,
      case 
        when base.product in ('Hydro', 'Solar', 'Geothermal', 'Combustible renewables', 'Renewables') 
        then true
        else false  
      end as is_renewable,
      base.production_gwh,
      lag(base.production_gwh) over (partition by base.country, base.product order by base.year, base.month) as production_gwh_previous_month,
      (base.production_gwh - production_gwh_previous_month) / production_gwh_previous_month as production_growth_pct
    from base_data as base
    left join countries_mapping as countries
    on base.country = countries.country_name

)

select * from final