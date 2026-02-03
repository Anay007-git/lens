const vscode = require('vscode');
const { exec } = require('child_process');
const path = require('path');

function activate(context) {
    console.log('LENS extension is now active!');

    let runQueryCommand = vscode.commands.registerCommand('lens.runQuery', function () {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No active editor found.');
            return;
        }

        const document = editor.document;
        if (document.languageId !== 'lens') {
            vscode.window.showErrorMessage('This is not a .lens file.');
            return;
        }

        const queryText = document.getText();
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '.';

        // Create output channel
        const outputChannel = vscode.window.createOutputChannel('LENS Output');
        outputChannel.show();
        outputChannel.appendLine(`--- Running LENS Query ---`);
        outputChannel.appendLine(queryText);
        outputChannel.appendLine(`--------------------------`);

        // Execute via Python CLI (to be implemented in cli/)
        const cliPath = path.join(workspaceFolder, 'cli', 'lens_cli.py');
        const cmd = `python "${cliPath}" -q "${queryText.replace(/"/g, '\\"').replace(/\n/g, ' ')}"`;

        exec(cmd, { cwd: workspaceFolder }, (error, stdout, stderr) => {
            if (error) {
                outputChannel.appendLine(`Error: ${error.message}`);
                return;
            }
            if (stderr) {
                outputChannel.appendLine(`Stderr: ${stderr}`);
            }
            outputChannel.appendLine(stdout);
        });
    });

    context.subscriptions.push(runQueryCommand);
}

function deactivate() { }

module.exports = {
    activate,
    deactivate
};
