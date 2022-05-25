{#
    This macro returns the description of the payment type
#}

{% macro update_airport_code(zone, else_col) %}

    case {{zone}}
        when "Newark Airport" then 'EWR'
        when "JFK Airport" then 'JFK'
        when "LaGuardia Airport" then 'LGA'
    else {{else_col}}
    end

{% endmacro %}