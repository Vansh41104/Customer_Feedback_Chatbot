from golden_query import GoldenQuery
from enum import StrEnum

TABLE_NAME = 'chatbot_data'

class Column(StrEnum):
    FEEDBACK = 'translated_comment'
    SERVICE_ADVISOR_NAME = 'agent_name'
    BRAND_NAME = 'brand_name'
    BRANCH = 'outlet_location'
    FEEDBACK_DATE = 'feedback_date'
    SURVEY_SOURCE = 'survey_source'
    PROMOTER = 'promoter'
    PASSIVE = 'passive'
    DETRACTOR = 'detractor'
    CUSTOMER_ID = 'customer_id'


golden_queries = [
    GoldenQuery(
        [
            'How many feedbacks do I have from the Body Shop campaign',
            'How many feedbacks do I have from the Body Shop survey',
        ],
        f"select count(*) as feedback_count from {TABLE_NAME} where {Column.SURVEY_SOURCE} = 'Body Shop'"
    ),
    GoldenQuery(
        [
            'List the top 3 things we are doing well',
            'List the top 3 things we are performing worst at',
            'List the main feedback we are getting',
            'List the main things we are doing well',
            'List the main things we are doing badly',
            'Summarise the things we are doing well'
        ],
        f"select {Column.FEEDBACK} from {TABLE_NAME}"
    ),
    GoldenQuery(
        'List the top things we are doing bad at in April 2023',
        [
            f"select {Column.FEEDBACK} from {TABLE_NAME} where {Column.FEEDBACK_DATE} >= '2023-04-01' where {Column.FEEDBACK_DATE} < '2023-05-01'",
            f"select {Column.FEEDBACK} from {TABLE_NAME} where {Column.FEEDBACK_DATE} >= '2023-04-01' where {Column.FEEDBACK_DATE} <= '2023-04-30'",
        ]
    ),
    GoldenQuery(
        'How many responses do we have by brand',
        f'select {Column.BRAND_NAME}, count(*) as feedback_count from {TABLE_NAME} group by {Column.BRAND_NAME}'
    ),
    GoldenQuery(
        'How many responses do we have by brand in January 2023',
        [
            f"select {Column.BRAND_NAME}, count(*) as feedback_count from {TABLE_NAME} where {Column.FEEDBACK_DATE} >= '2023-01-01' where {Column.FEEDBACK_DATE} < '2023-02-01' group by {Column.BRAND_NAME}",
            f"select {Column.BRAND_NAME}, count(*) as feedback_count from {TABLE_NAME} where {Column.FEEDBACK_DATE} >= '2023-01-01' where {Column.FEEDBACK_DATE} <= '2023-01-31' group by {Column.BRAND_NAME}",
        ]
    ),
    GoldenQuery(
        'How many service providers work with Infiniti',
        f"select count(distinct {Column.SERVICE_ADVISOR_NAME}) as total_advisor_count from {TABLE_NAME} where {Column.BRAND_NAME} = 'Infiniti'"
    ),
    GoldenQuery(
        [
            'What is the best feedback from customers that bought a Nissan',
            'Summarise the feedback for Nissan this month'
        ],
        f"select {Column.FEEDBACK} from {TABLE_NAME} where {Column.BRAND_NAME} = 'Nissan'"
    ),
    GoldenQuery(
        'What is the worst feedback from my NISSAN Service Airport Road branch',
        f"select {Column.FEEDBACK} from {TABLE_NAME} where {Column.BRANCH} = 'NISSAN Service Airport Road'"
    ),
    GoldenQuery(
        'What is the worst feedback from my INFINITI Service Mussafah branch',
        f"select {Column.FEEDBACK} from {TABLE_NAME} where {Column.BRANCH} = 'INFINITI Service Mussafah'"
    ),
    GoldenQuery(
        'What was the best feedback about service representative Khalil Ur Rahman',
        f"select {Column.FEEDBACK} from {TABLE_NAME} where {Column.SERVICE_ADVISOR_NAME} = 'Khalil Ur Rahman'"
    ),
    GoldenQuery(
        'How many customer responses do you have for the brand infiniti',
        f"select count(*) as feedback_count from {TABLE_NAME} where {Column.BRAND_NAME} = 'Infiniti'"
    ),
    GoldenQuery(
        'List the names of all agents working with Nissan',
        f"select {Column.SERVICE_ADVISOR_NAME} from {TABLE_NAME} where {Column.BRAND_NAME} = 'Nissan' group by {Column.SERVICE_ADVISOR_NAME}"
    ),
    GoldenQuery(
        'How many detractors did we have',
        f"select count(*) from {TABLE_NAME} where {Column.DETRACTOR} = 1"
    ),
    GoldenQuery(
        [
            'what are the most common complaints about staff members',
            'What are my detractors unhappy with?'
        ],
        f"select {Column.FEEDBACK} from {TABLE_NAME} where {Column.DETRACTOR} = 1"
    ),
    GoldenQuery(
        'What is the NPS score',
        f"select ((select count(*) from {TABLE_NAME} where {Column.PROMOTER} = 1) - (select count(*) from {TABLE_NAME} where {Column.DETRACTOR} = 1)) * 100 / (select count(*) from {TABLE_NAME})"
    ),
    GoldenQuery(
        'What is the NPS score in March 2023',
        f"select ((select count(*) from {TABLE_NAME} where {Column.PROMOTER} = 1 and {Column.FEEDBACK_DATE} >= '2023-03-01' and {Column.FEEDBACK_DATE} < '2023-04-01') - (select count(*) from {TABLE_NAME} where {Column.DETRACTOR} = 1 and {Column.FEEDBACK_DATE} >= '2023-03-01' and {Column.FEEDBACK_DATE} < '2023-04-01')) * 100 / (select count(*) from {TABLE_NAME} where {Column.FEEDBACK_DATE} >= '2023-03-01' and {Column.FEEDBACK_DATE} < '2023-04-01')"
    ),
    GoldenQuery(
        'What is the NPS score for Nissan',
        f"select ((select count(*) from {TABLE_NAME} where {Column.PROMOTER} = 1 and {Column.BRAND_NAME} = 'Nissan') - (select count(*) from {TABLE_NAME} where {Column.DETRACTOR} = 1 and {Column.BRAND_NAME} = 'Nissan')) * 100 / (select count(*) from {TABLE_NAME} where {Column.BRAND_NAME} = 'Nissan')"
    ),
    GoldenQuery(
        'What is the NPS score for the Body Shop campaign',
        f"select ((select count(*) from {TABLE_NAME} where {Column.PROMOTER} = 1 and {Column.BRAND_NAME} = 'Nissan' and {Column.SURVEY_SOURCE} = 'Body Shop') - (select count(*) from {TABLE_NAME} where {Column.DETRACTOR} = 1 and {Column.BRAND_NAME} = 'Nissan' and {Column.SURVEY_SOURCE} = 'Body Shop')) * 100 / (select count(*) from {TABLE_NAME} where {Column.BRAND_NAME} = 'Nissan' and {Column.SURVEY_SOURCE} = 'Body Shop')"
    ),
    GoldenQuery(
        'What is the NPS score for Nissan customer from the the Body Shop campaign',
        f"select ((select count(*) from {TABLE_NAME} where {Column.PROMOTER} = 1 and {Column.SURVEY_SOURCE} = 'Body Shop') - (select count(*) from {TABLE_NAME} where {Column.DETRACTOR} = 1 and {Column.SURVEY_SOURCE} = 'Body Shop')) * 100 / (select count(*) from {TABLE_NAME} where {Column.SURVEY_SOURCE} = 'Body Shop')"
    ),
    GoldenQuery(
        'What was the NPS score for Nissan in March 2023',
        f"select ((select count(*) from {TABLE_NAME} where {Column.PROMOTER} = 1 and {Column.BRAND_NAME} = 'Nissan' and {Column.FEEDBACK_DATE} >= '2023-03-01' and {Column.FEEDBACK_DATE} < '2023-04-01') - (select count(*) from {TABLE_NAME} where {Column.DETRACTOR} = 1 and {Column.BRAND_NAME} = 'Nissan' and {Column.FEEDBACK_DATE} >= '2023-03-01' and {Column.FEEDBACK_DATE} < '2023-04-01')) * 100 / (select count(*) from {TABLE_NAME} where {Column.BRAND_NAME} = 'Nissan' and {Column.FEEDBACK_DATE} >= '2023-03-01' and {Column.FEEDBACK_DATE} < '2023-04-01')"
    ),
    GoldenQuery(
        'What was the NPS score for the INFINITI Service Mussafah branch in March 2023',
        f"select ((select count(*) from {TABLE_NAME} where {Column.PROMOTER} = 1 and {Column.BRANCH} = 'INFINITI Service Mussafah' and {Column.FEEDBACK_DATE} >= '2023-03-01' and {Column.FEEDBACK_DATE} < '2023-04-01') - (select count(*) from {TABLE_NAME} where {Column.DETRACTOR} = 1 and {Column.BRANCH} = 'INFINITI Service Mussafah' and {Column.FEEDBACK_DATE} >= '2023-03-01' and {Column.FEEDBACK_DATE} < '2023-04-01')) * 100 / (select count(*) from {TABLE_NAME} where {Column.BRANCH} = 'INFINITI Service Mussafah' and {Column.FEEDBACK_DATE} >= '2023-03-01' and {Column.FEEDBACK_DATE} < '2023-04-01')"
    ),
    GoldenQuery(
        [
            'What is the NPS score for this month',
            'What is my score for this month'
        ],
        f"select ((select count(*) from {TABLE_NAME} where {Column.PROMOTER} = 1 and strftime('%Y', {Column.FEEDBACK_DATE}) = strftime('%Y', 'now')) - (select count(*) from {TABLE_NAME} where {Column.DETRACTOR} = 1 and strftime('%Y', {Column.FEEDBACK_DATE}) = strftime('%Y', 'now'))) * 100 / (select count(*) from {TABLE_NAME} where strftime('%Y', {Column.FEEDBACK_DATE}) = strftime('%Y', 'now'))"
    ),
    GoldenQuery(
        [
            'What is the NPS score for this year',
            'What is the NPS score year to date',
            'What is my score for this year'
        ],
        f"select ((select count(*) from {TABLE_NAME} where {Column.PROMOTER} = 1 and strftime('%Y', {Column.FEEDBACK_DATE}) = strftime('%Y', 'now')) - (select count(*) from {TABLE_NAME} where {Column.DETRACTOR} = 1 and strftime('%Y', {Column.FEEDBACK_DATE}) = strftime('%Y', 'now'))) * 100 / (select count(*) from {TABLE_NAME} where strftime('%Y', {Column.FEEDBACK_DATE}) = strftime('%Y', 'now'))"
    ),
    GoldenQuery(
        'What was the NPS score for the INFINITI Service Mussafah branch',
        f"select ((select count(*) from {TABLE_NAME} where {Column.PROMOTER} = 1 and {Column.BRANCH} = 'INFINITI Service Mussafah') - (select count(*) from {TABLE_NAME} where {Column.DETRACTOR} = 1 and {Column.BRANCH} = 'INFINITI Service Mussafah')) * 100 / (select count(*) from {TABLE_NAME} where {Column.BRANCH} = 'INFINITI Service Mussafah')"
    ),
    GoldenQuery(
        [
            'What was the NPS score for the Body Shop survey',
            'What was the NPS score for the Body Shop campaign',
        ],
        f"select ((select count(*) from {TABLE_NAME} where {Column.PROMOTER} = 1 and {Column.SURVEY_SOURCE} = 'Body Shop') - (select count(*) from {TABLE_NAME} where {Column.DETRACTOR} = 1 and {Column.SURVEY_SOURCE} = 'Body Shop')) * 100 / (select count(*) from {TABLE_NAME} where {Column.SURVEY_SOURCE} = 'Body Shop')"
    ),
    GoldenQuery(
        [
            'What are the number of passives this month?',
            'What are my number of passives this month?'
        ],
        f"select count(*) from {TABLE_NAME} where {Column.PASSIVE} = 1 and {Column.FEEDBACK_DATE} >= date('now','start of month') and {Column.FEEDBACK_DATE} < date('now')"
    ),
    GoldenQuery(
        'What are the number of passives last month?',
        f"select count(*) from {TABLE_NAME} where {Column.PASSIVE} = 1 and {Column.FEEDBACK_DATE} >= date('now','start of month','-1 month')and {Column.FEEDBACK_DATE} < date('now','start of month')"
    ),
    GoldenQuery(
        'What are the number of passives year to date?',
        f"select count(*) from {TABLE_NAME} where {Column.PASSIVE} = 1 and strftime('%Y', {Column.FEEDBACK_DATE}) = strftime('%Y', 'now')"
    ),
    GoldenQuery(
        'What are the number of passives in the last quarter?',
        f"select count(*) from {TABLE_NAME} where {Column.PASSIVE} = 1  and {Column.FEEDBACK_DATE} >= date('now','start of month','-3 months') and {Column.FEEDBACK_DATE} < date('now','start of month')"
    ),
    GoldenQuery(
        'Number of promoters / passives / detractors?',
        f"select sum{Column.PROMOTER} as total_promoters, sum{Column.PASSIVE} as total_passives, sum{Column.DETRACTOR} as total_detractors from {TABLE_NAME}"
    ),
    GoldenQuery(
        'Number of promoters / passives / detractors for this month?',
        f"select sum{Column.PROMOTER} as total_promoters, sum{Column.PASSIVE} as total_passives, sum{Column.DETRACTOR} as total_detractors from {TABLE_NAME} where {Column.FEEDBACK_DATE} >= date('now','start of month') and {Column.FEEDBACK_DATE} < date('now');"
    ),
    GoldenQuery(
        'Number of promoters / passives / detractors for this quarter?',
        f"select sum{Column.PROMOTER} as total_promoters, sum{Column.PASSIVE} as total_passives, sum{Column.DETRACTOR} as total_detractors from {TABLE_NAME} where {Column.FEEDBACK_DATE} >= date('now','start of month', '-3 months') and {Column.FEEDBACK_DATE} < date('now');"
    ),
    GoldenQuery(
        'Number of promoters / passives / detractors year to date?',
        f"select sum{Column.PROMOTER} as total_promoters, sum{Column.PASSIVE} as total_passives, sum{Column.DETRACTOR} as total_detractors from {TABLE_NAME} where strftime('%Y', {Column.FEEDBACK_DATE}) = strftime('%Y', 'now');"
    )
]
