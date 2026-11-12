// ============================================================
// Script    : ProbeSettingsExportNodes
// Purpose   : Find out which settings node exports the keyboard shortcuts
// You learn : CommandLineInterpreter, running an Eplan action with parameters, checking its result
// Level     : Beginner
// Tested in : Not yet run (Draft)
// Author    : Justin Walz
// License   : MIT (see LICENSE in the repo root)
// ============================================================
//
// Safe to run: it only EXPORTS. It writes a few small test files to your
// temp folder and never imports or changes any Eplan setting.
//
// For each settings node below it runs the XSettingsExport action, then
// reports whether Eplan said it worked, how big the file is, and whether
// the shortcut keys are inside. This tells us how to build a one-click
// import for the shortcut keys.

using System;
using System.Drawing;
using System.IO;
using System.Text;
using System.Windows.Forms;
using Eplan.EplApi.ApplicationFramework;
using Eplan.EplApi.Scripting;

public class ProbeSettingsExportNodes
{
    [Start]
    public void Run()
    {
        string[] nodes = new string[]
        {
            "USER",
            "USER.SYSTEM",
            "USER.SYSTEM.GUI",
            "USER.SYSTEM.GUI.Shortcuts"
        };

        string folder = Path.Combine(Path.GetTempPath(), "EplanShortcutProbe");
        StringBuilder sb = new StringBuilder();
        sb.AppendLine("Probe of XSettingsExport nodes");
        sb.AppendLine("Run at: " + DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"));
        sb.AppendLine("Test files go to: " + folder);
        sb.AppendLine();

        try
        {
            Directory.CreateDirectory(folder);
        }
        catch (Exception ex)
        {
            sb.AppendLine("Could not create the test folder: " + ex.Message);
            ShowWindow(sb.ToString());
            return;
        }

        for (int i = 0; i < nodes.Length; i++)
        {
            TryNode(nodes[i], Path.Combine(folder, "node" + (i + 1) + ".xml"), sb);
        }

        string text = sb.ToString();
        try
        {
            File.WriteAllText(Path.Combine(folder, "result.txt"), text, Encoding.UTF8);
        }
        catch (Exception)
        {
            // Saving the result is optional.
        }
        ShowWindow(text);
    }

    // Runs one export and describes what came out.
    private void TryNode(string node, string file, StringBuilder sb)
    {
        sb.AppendLine("##### node = " + node);
        try
        {
            if (File.Exists(file))
            {
                File.Delete(file);
            }

            string command = "XSettingsExport /node:" + node + " /XMLFile:\"" + file + "\"";
            sb.AppendLine("Command: " + command);

            CommandLineInterpreter cli = new CommandLineInterpreter();
            bool ok = cli.Execute(command);
            sb.AppendLine("Eplan returned: " + ok);

            if (!File.Exists(file))
            {
                sb.AppendLine("No file was written.");
            }
            else
            {
                string xml = File.ReadAllText(file);
                sb.AppendLine("File size: " + xml.Length + " characters");
                sb.AppendLine("Contains shortcut section: " + (xml.IndexOf("name=\"Shortcuts\"", StringComparison.Ordinal) >= 0));
                sb.AppendLine("Contains Ctrl+Alt+Z: " + (xml.IndexOf("Ctrl+Alt+Z", StringComparison.Ordinal) >= 0));
            }
        }
        catch (Exception ex)
        {
            sb.AppendLine("Failed: " + ex.Message);
        }
        sb.AppendLine();
    }

    private void ShowWindow(string text)
    {
        Form form = new Form();
        form.Text = "Settings export probe";
        form.StartPosition = FormStartPosition.CenterScreen;
        form.Size = new Size(760, 560);

        TextBox box = new TextBox();
        box.Multiline = true;
        box.ReadOnly = true;
        box.ScrollBars = ScrollBars.Both;
        box.WordWrap = false;
        box.Font = new Font("Consolas", 9f);
        box.Dock = DockStyle.Fill;
        box.Text = text;
        box.Select(0, 0);

        Panel bottom = new Panel();
        bottom.Dock = DockStyle.Bottom;
        bottom.Height = 44;

        Button copy = new Button();
        copy.Text = "Copy";
        copy.SetBounds(10, 8, 90, 28);
        string toCopy = text;
        copy.Click += new System.EventHandler(delegate(object s, System.EventArgs e)
        {
            Clipboard.SetText(toCopy);
        });

        Button close = new Button();
        close.Text = "Close";
        close.SetBounds(110, 8, 90, 28);
        close.Click += new System.EventHandler(delegate(object s, System.EventArgs e)
        {
            form.Close();
        });

        bottom.Controls.Add(copy);
        bottom.Controls.Add(close);
        form.Controls.Add(box);
        form.Controls.Add(bottom);
        form.ShowDialog();
        form.Dispose();
    }
}
