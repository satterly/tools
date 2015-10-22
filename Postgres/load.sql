TRUNCATE TABLE
antispam_badword                       ,
auth_group                             ,
auth_group_permissions                 ,
auth_message                           ,
auth_permission                        ,
auth_user                              ,
auth_user_groups                       ,
auth_user_user_permissions             ,
avatars_avatar                         ,
cachetable                             ,
clients_client                         ,
clients_comment                        ,
comments_comment                       ,
comments_commenthighlight              ,
comments_commentrecommendations        ,
comments_discussion                    ,
comments_discussion_tags               ,
comments_namespace                     ,
comments_rating                        ,
comments_tag                           ,
django_admin_log                       ,
django_content_type                    ,
django_session                         ,
django_site                            ,
importer_pluckimportedcomment          ,
importer_pluckimportedrating           ,
importer_pluckimportedrecommendation   ,
importer_pluckimportedreview           ,
moderation_abusecategory               ,
moderation_abusereport                 ,
moderation_action                      ,
moderation_applicationpermissions      ,
moderation_ipaddressnotes              ,
moderation_ipsblockedfromreportingabuse,
moderation_moderatorprofile            ,
moderation_queues_moderationqueue      ,
moderation_queues_moderationrequest    ,
moderation_sanction                    ,
profiles_badge                         ,
profiles_profile                       ,
profiles_profile_badges                ,
recommendations_recommendation         ,
social_auth_association                ,
social_auth_nonce                      ,
social_auth_usersocialauth             ,
south_migrationhistory                 ,
switchboard_state                      ,
switchboard_switch                     ;

\copy django_site from '/tmp/django_site.sql';
\copy django_content_type from '/tmp/django_content_type.sql';

\copy auth_group from '/tmp/auth_group.sql';
\copy auth_permission from '/tmp/auth_permission.sql';
\copy auth_group_permissions from '/tmp/auth_group_permissions.sql';

\copy auth_user from '/tmp/auth_user.sql';
\copy auth_user_groups from '/tmp/auth_user_groups.sql';
\copy auth_user_user_permissions from '/tmp/auth_user_user_permissions.sql';

\copy antispam_badword from '/tmp/antispam_badword.sql';

\copy comments_namespace from '/tmp/comments_namespace.sql';
\copy comments_tag from '/tmp/comments_tag.sql';
\copy profiles_badge from '/tmp/profiles_badge.sql';

\copy comments_discussion from '/tmp/comments_discussion.sql';
\copy profiles_profile from '/tmp/profiles_profile.sql';
\copy profiles_profile_badges from '/tmp/profiles_profile_badges.sql';
\copy comments_comment from '/tmp/comments_comment.sql';

\copy moderation_abusecategory from '/tmp/moderation_abusecategory.sql';
-- \copy moderation_abusereport from '/tmp/moderation_abusereport.sql';
\copy moderation_action from '/tmp/moderation_action.sql';
\copy moderation_applicationpermissions from '/tmp/moderation_applicationpermissions.sql';
\copy moderation_ipaddressnotes from '/tmp/moderation_ipaddressnotes.sql';
\copy moderation_ipsblockedfromreportingabuse from '/tmp/moderation_ipsblockedfromreportingabuse.sql';
-- \copy moderation_moderatorprofile from '/tmp/moderation_moderatorprofile.sql';
\copy moderation_queues_moderationqueue from '/tmp/moderation_queues_moderationqueue.sql';
-- \copy moderation_queues_moderationrequest from '/tmp/moderation_queues_moderationrequest.sql';
\copy moderation_sanction from '/tmp/moderation_sanction.sql';

\copy switchboard_switch from '/tmp/switchboard_switch.sql';
\copy switchboard_state from '/tmp/switchboard_state.sql';
