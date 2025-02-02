with base_data as (

    select
        country,
        code_time,
        time,
        year,
        month,
        month_name,
        product,
        value,
        display_order,
        year_to_date
    from {{ source('electricity', 'electricity_production') }}

),

final as (

    select
        country,
        year::int as year,
        month::int as month,
        product,
        value as production_gwh
    from base_data

)

select * from final