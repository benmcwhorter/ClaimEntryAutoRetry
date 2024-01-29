/*  select 
  top 3
  internal_client_key, payload
  FROM [ARKLog].[ClaimEntry].[vEntryLog] l
  where logmsg like '%500%' --system error
  and not exists (	--another attempt doesnt exist
					select * from [ARKLog].[ClaimEntry].[vEntryLog] l2
					where l.BatchId <> l2.batchid --different batchid
					and l.claimkey = l2.claimkey --same claim
					)
*/

  select internalclientkey as 'internal_client_key', payload, batchid--, CreateAt
  FROM [ARKLog].[ClaimEntry].[vEntryLog] l0
  where l0.logmsg = 'Claim received.'
 -- and createat >= '7/1/2023'
  and exists
	(
	  select *
	  FROM [ARKLog].[ClaimEntry].[vEntryLog] l
	  where 
	  logmsg = 'Claim persistence failed. Errors: You cannot insert claims for an audit that you are not assigned to or does not exist.'
	  --logmsg like '%500%' --system error
	  --logMsg like '%Lag' --lag exclusion
	  
	  and not exists (	--another attempt different batch doesnt exist
						select * from [ARKLog].[ClaimEntry].[vEntryLog] l2
						where l.BatchId <> l2.batchid --different batchid
						and l.claimkey = l2.claimkey --same claim
						)
	 /*and not exists	(	--another attempt isnt successful
						select * from [ARKLog].[ClaimEntry].[vEntryLog] l3
						where l.BatchId = l3.batchid --different batchid
						and l.claimkey = l3.claimkey --same claim
						and l3.LogMsg = 'Post Commit persisted.'
						)*/
	--  and logmsg not like '%model%not found%' --not actually model error
	  and l.BatchId = l0.batchid
	  and l.CorrelationId = l0.CorrelationId
	)
	and createat >= '9/20/2023'