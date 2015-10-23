#!/bin/bash

SRC_DBNAME=discussion
SRC_DBHOST=localhost
SRC_DBPORT=8432
SRC_DBUSER=discussion_app

DEST_DBNAME=discussion
DEST_DBHOST=localhost
DEST_DBPORT=5432
DEST_DBUSER=pgowner

set -f
set +e

echo "Dumping data to $SRC_DBHOST:$SRC_DBPORT"

psql \
  -v ON_ERROR_STOP=1 \
  -U $SRC_DBUSER \
  -h $SRC_DBHOST \
  -p $SRC_DBPORT \
  $SRC_DBNAME << SQL
\copy (select * from django_content_type) to '/tmp/django_content_type.sql';

\copy (select * from auth_group) to '/tmp/auth_group.sql';
\copy (select * from auth_permission) to '/tmp/auth_permission.sql';
\copy (select * from auth_group_permissions where group_id!=35) to '/tmp/auth_group_permissions.sql';

\copy (select * from auth_user where username in ('nick.satterly', 'nicolas.long')) to '/tmp/auth_user.sql';
\copy (select * from auth_user_groups where user_id in (select id from auth_user where username in ('nick.satterly', 'nicolas.long'))) to '/tmp/auth_user_groups.sql';
\copy (select * from auth_user_user_permissions where user_id in (select id from auth_user where username in ('nick.satterly', 'nicolas.long'))) to '/tmp/auth_user_user_permissions.sql';

\copy (select link_urls_only,word,id,(select id from auth_user where username='nick.satterly'),created from antispam_badword) to '/tmp/antispam_badword.sql';

\copy (select * from comments_namespace) to '/tmp/comments_namespace.sql';
\copy (select * from comments_tag) to '/tmp/comments_tag.sql';
\copy (select * from profiles_badge) to '/tmp/profiles_badge.sql';

\copy (select * from profiles_profile_badges where profile_id in (select posted_by_id from comments_comment where discussion_id=(select id from comments_discussion where key='/p/4df2e'))) to '/tmp/profiles_profile_badges.sql';

\copy (select primary_tag_id, closed_after, url, premoderated, title, namespace_id, created_on, dn_total_comment_count, key, id, dn_invisible_comment_count, anon_user_rating_count, anon_user_rating_total, dn_reg_user_rating_count,  dn_reg_user_rating_total, creating_comment_id, last_updated, NULL, display_threaded, dn_top_level_comment_count, status, watched from comments_discussion where key='/p/4df2e') to '/tmp/comments_discussion.sql';
\copy (select distinct pp.username, pp.interests, NULL, pp.user_id, pp.pluck_avatar_url, pp.lowercase_username, pp.gender, pp.last_updated_on, pp.dob, pp.created_on, pp.about_me, pp.location, pp.web_page, pp.real_name, pp.id, pp.last_ip_address, pp.total_comment_count, pp.vanity_url, pp.is_social, pp.last_exported_on from profiles_profile pp inner join comments_comment cc on pp.id=cc.posted_by_id where cc.discussion_id=(select id from comments_discussion where key='/p/4df2e')) to '/tmp/profiles_profile.sql';
\copy (select * from comments_comment where discussion_id=(select id from comments_discussion where key='/p/4df2e')) to '/tmp/comments_comment.sql';

\copy (select * from moderation_abusecategory) to '/tmp/moderation_abusecategory.sql';
\copy (select * from moderation_abusereport where comment_id in (select id from comments_comment where discussion_id=(select id from comments_discussion where key='/p/4df2e'))) to '/tmp/moderation_abusereport.sql';
\copy (select comment_id,profile_id,note,created_on,abuse_report_id,'403',avatar_id,sanction_id,type,id,discussion_id,avatar_api_id from moderation_action where comment_id in (select id from comments_comment where discussion_id=(select id from comments_discussion where key='/p/4df2e'))) to '/tmp/moderation_action.sql';
\copy (select * from moderation_applicationpermissions) to '/tmp/moderation_applicationpermissions.sql';
\copy (select id,'403',created_on,note,ip_address,action from moderation_ipaddressnotes) to '/tmp/moderation_ipaddressnotes.sql';
\copy (select id,ip,block_start,block_end,'403' from moderation_ipsblockedfromreportingabuse) to '/tmp/moderation_ipsblockedfromreportingabuse.sql';
-- \copy (select * from moderation_moderatorprofile) to '/tmp/moderation_moderatorprofile.sql';
\copy (select * from moderation_queues_moderationqueue) to '/tmp/moderation_queues_moderationqueue.sql';
-- \copy (select * from moderation_queues_moderationrequest) to '/tmp/moderation_queues_moderationrequest.sql';
\copy (select created_on,sanction_until,'403',note,user_id,id,sanction_type from moderation_sanction where user_id in (select posted_by_id from comments_comment where discussion_id=(select id from comments_discussion where key='/p/4df2e'))) to '/tmp/moderation_sanction.sql';

\copy (select * from switchboard_switch) to '/tmp/switchboard_switch.sql';
\copy (select * from switchboard_state) to '/tmp/switchboard_state.sql';
SQL

echo "Loading dumped data to $DEST_DBHOST:$DEST_DBPORT"

psql \
  -v ON_ERROR_STOP=1 \
  -U $DEST_DBUSER \
  -h $DEST_DBHOST \
  -p $DEST_DBPORT \
  $DEST_DBNAME << SQL
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
SQL