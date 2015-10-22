
\copy (select * from django_site) to '/tmp/django_site.sql';
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

/*
 public | django_content_type                     | table | x
 public | django_site                             | table | x

 public | auth_group                              | table | x
 public | auth_group_permissions                  | table | x
 public | auth_permission                         | table | x
 public | auth_user                               | table | x
 public | auth_user_groups                        | table | x
 public | auth_user_user_permissions              | table | x

 public | antispam_badword                        | table | x

 public | comments_namespace                      | table | x
 public | comments_tag                            | table | x

 public | profiles_badge                          | table | x
 public | profiles_profile_badges                 | table | x

 public | comments_discussion                     | table | x
 public | profiles_profile                        | table | x
 public | comments_comment                        | table | x

 public | comments_commenthighlight               | table | pgowner
 public | comments_commentrecommendations         | table | pgowner
 public | comments_discussion_tags                | table | pgowner
 public | comments_rating                         | table | pgowner

 public | moderation_abusecategory                | table | x
 public | moderation_abusereport                  | table | x
 public | moderation_action                       | table | x
 public | moderation_applicationpermissions       | table | x
 public | moderation_ipaddressnotes               | table | x
 public | moderation_ipsblockedfromreportingabuse | table | x
 public | moderation_moderatorprofile             | table | x
 public | moderation_queues_moderationqueue       | table | x
 public | moderation_queues_moderationrequest     | table | x
 public | moderation_sanction                     | table | x

 public | switchboard_state                       | table | x
 public | switchboard_switch                      | table | x
 */