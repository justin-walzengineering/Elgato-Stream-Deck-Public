// ============================================================
// Script    : ProbeSettingsActions
// Purpose   : List the parameters of Eplan's settings export and import actions
// You learn : ActionManager, FindAction, reading action parameters, showing results in a window
// Level     : Beginner
// Tested in : Not yet run (Draft)
// Author    : Justin Walz
// License   : MIT (see LICENSE in the repo root)
// ============================================================
//
// Read-only. It changes nothing in Eplan. It asks Eplan which parameters
// the settings export/import actions accept, and shows the answer in a
// window you can copy from. The result tells us how to build a one-click
// "import shortcut keys" script.

using System;
using System.Collections;
using System.Drawing;
using System.IO;
using System.Reflection;
using System.Text;
using System.Windows.Forms;
using Eplan.EplApi.ApplicationFramework;
using Eplan.EplApi.Scripting;

public class ProbeSettingsActions
{
    [Start]
    public void Run()
    {
        StringBuilder sb = new StringBuilder();
        sb.AppendLine("Probe of Eplan settings actions");
        sb.AppendLine("Run at: " + DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"));
        sb.AppendLine();

        string[] names = new string[] { "XSettingsExport", "XSettingsImport" };
        for (int i = 0; i < names.Length; i++)
        {
            DescribeAction(names[i], sb);
        }

        string text = sb.ToString();
        string savedTo = TrySave(text);
        ShowWindow(text, savedTo);
    }

    // Looks up one action and writes what we can learn about it.
    private void DescribeAction(string actionName, StringBuilder sb)
    {
        sb.AppendLine("##### " + actionName + " #####");
        try
        {
            ActionManager manager = new ActionManager();
            Eplan.EplApi.ApplicationFramework.Action action = manager.FindAction(actionName);
            if (action == null)
            {
                sb.AppendLine("Action not found.");
                sb.AppendLine();
                return;
            }

            ArrayList parameters = action.ActionProperties.GetParameterProperties();
            sb.AppendLine("Parameter count: " + parameters.Count);
            for (int i = 0; i < parameters.Count; i++)
            {
                object item = parameters[i];
                sb.AppendLine("--- parameter " + (i + 1) + " (" + item.GetType().Name + ")");
                DumpProperties(item, sb);
            }
        }
        catch (Exception ex)
        {
            sb.AppendLine("Could not read this action: " + ex.Message);
        }
        sb.AppendLine();
    }

    // Writes every simple public property of an object, using reflection
    // so the script does not depend on the exact type name.
    private void DumpProperties(object item, StringBuilder sb)
    {
        PropertyInfo[] props = item.GetType().GetProperties(BindingFlags.Public | BindingFlags.Instance);
        for (int i = 0; i < props.Length; i++)
        {
            if (props[i].GetIndexParameters().Length != 0)
            {
                continue;
            }
            string value;
            try
            {
                object v = props[i].GetValue(item, null);
                value = (v == null) ? "(none)" : v.ToString();
            }
            catch (Exception)
            {
                value = "(could not read)";
            }
            sb.AppendLine("    " + props[i].Name + " = " + value);
        }
    }

    // Saves a copy to the user's temp folder; returns the path, or an empty string.
    private string TrySave(string text)
    {
        try
        {
            string path = Path.Combine(Path.GetTempPath(), "EplanSettingsActionsProbe.txt");
            File.WriteAllText(path, text, Encoding.UTF8);
            return path;
        }
        catch (Exception)
        {
            return "";
        }
    }

    // A simple window with the result in a text box and a Copy button.
    private void ShowWindow(string text, string savedTo)
    {
        Form form = new Form();
        form.Text = "Settings actions probe";
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

        Label where = new Label();
        where.Text = (savedTo.Length > 0) ? "Also saved to: " + savedTo : "";
        where.SetBounds(215, 14, 520, 20);

        bottom.Controls.Add(copy);
        bottom.Controls.Add(close);
        bottom.Controls.Add(where);
        form.Controls.Add(box);
        form.Controls.Add(bottom);
        form.ShowDialog();
        form.Dispose();
    }
}
