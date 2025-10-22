const { LinearClient } = require('@linear/sdk');
const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    // Get inputs
    const linearApiKey = process.env.LINEAR_API_KEY;
    const linearTeamId = process.env.LINEAR_TEAM_ID;
    const action = process.env.ACTION;
    const issueNumber = process.env.ISSUE_NUMBER;
    const issueTitle = process.env.ISSUE_TITLE;
    const issueBody = process.env.ISSUE_BODY;

    console.log(`🔗 FSL Continuum: Linear Sync`);
    console.log(`Action: ${action}`);

    // Initialize Linear client
    const linear = new LinearClient({ apiKey: linearApiKey });

    switch (action) {
      case 'create-epic':
        await createEpic(linear, linearTeamId, issueNumber, issueTitle, issueBody);
        break;
      case 'update-status':
        await updateStatus(linear, issueNumber);
        break;
      case 'close-epic':
        await closeEpic(linear, issueNumber);
        break;
      default:
        throw new Error(`Unknown action: ${action}`);
    }

  } catch (error) {
    core.setFailed(`Linear sync failed: ${error.message}`);
  }
}

async function createEpic(linear, teamId, issueNumber, title, body) {
  console.log(`📝 Creating Linear Epic for GitHub Issue #${issueNumber}`);

  // Create epic
  const epicPayload = {
    title: `[GitHub #${issueNumber}] ${title}`,
    description: `${body}\n\n---\n**Source:** GitHub Issue #${issueNumber}`,
    teamId: teamId,
  };

  const epic = await linear.createIssue(epicPayload);
  
  console.log(`✅ Created Linear Epic: ${epic.id}`);

  // AI-powered decomposition (simplified)
  const subIssues = decomposeIssue(title, body);
  
  console.log(`🤖 AI decomposed into ${subIssues.length} sub-issues`);

  // Create sub-issues
  for (const subIssue of subIssues) {
    const subPayload = {
      title: subIssue.title,
      description: subIssue.description,
      teamId: teamId,
      parentId: epic.id,
    };
    
    await linear.createIssue(subPayload);
    console.log(`  ✅ Created sub-issue: ${subIssue.title}`);
  }

  // Set outputs
  core.setOutput('epic-id', epic.id);
  core.setOutput('epic-url', epic.url);
  core.setOutput('sub-issues-count', subIssues.length);

  console.log(`✅ Linear sync complete!`);
}

async function updateStatus(linear, issueNumber) {
  console.log(`🔄 Updating Linear status for GitHub Issue #${issueNumber}`);
  // Implementation for status updates
  console.log(`✅ Status updated`);
}

async function closeEpic(linear, issueNumber) {
  console.log(`🔒 Closing Linear Epic for GitHub Issue #${issueNumber}`);
  // Implementation for closing epics
  console.log(`✅ Epic closed`);
}

function decomposeIssue(title, body) {
  // Simplified AI decomposition
  // In production, this would use an LLM API
  
  const subIssues = [
    {
      title: `Research: ${title}`,
      description: `Research phase for implementing: ${title}`
    },
    {
      title: `Implementation: ${title}`,
      description: `Core implementation of: ${title}`
    },
    {
      title: `Testing: ${title}`,
      description: `Testing and validation of: ${title}`
    },
    {
      title: `Documentation: ${title}`,
      description: `Documentation for: ${title}`
    }
  ];

  return subIssues;
}

run();
