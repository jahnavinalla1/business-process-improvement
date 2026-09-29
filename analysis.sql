-- name: team_performance
SELECT team,COUNT(*) requests,
 ROUND(AVG(intake_hours+review_hours+approval_hours+execution_hours+rework_hours),2) mean_cycle_hours,
 ROUND(100.0*AVG(CASE WHEN intake_hours+review_hours+approval_hours+execution_hours+rework_hours<=72 THEN 1 ELSE 0 END),2) sla_pct,
 ROUND(100.0*AVG(rework),2) rework_pct
FROM requests GROUP BY team ORDER BY mean_cycle_hours DESC;
-- name: route_mix
SELECT team,route,COUNT(*) requests,
 ROUND(AVG(intake_hours+review_hours+approval_hours+execution_hours+rework_hours),2) mean_cycle_hours,
 ROUND(AVG(review_hours),2) mean_review_hours
FROM requests GROUP BY team,route ORDER BY team,route;
-- name: stages
SELECT 'Intake' stage,ROUND(AVG(intake_hours),2) mean_elapsed_hours FROM requests
UNION ALL SELECT 'Review',ROUND(AVG(review_hours),2) FROM requests
UNION ALL SELECT 'Approval',ROUND(AVG(approval_hours),2) FROM requests
UNION ALL SELECT 'Execution',ROUND(AVG(execution_hours),2) FROM requests
UNION ALL SELECT 'Rework',ROUND(AVG(rework_hours),2) FROM requests;
-- name: ranked_cycle_times
SELECT request_id,team,intake_hours+review_hours+approval_hours+execution_hours+rework_hours cycle_hours,
 ROW_NUMBER() OVER(ORDER BY intake_hours+review_hours+approval_hours+execution_hours+rework_hours,request_id) position,
 COUNT(*) OVER() total
FROM requests ORDER BY cycle_hours,request_id;
