// ============================================================
// Script    : ImportShortcutKeys
// Purpose   : Import a shortcut-keys XML file into Eplan with one click, after an optional backup of your current shortcuts.
// You learn : Running Eplan's settings export/import actions, a themed window, backing up before a risky change, checking the result afterwards
// Level     : Intermediate
// Version   : 1.0.0
// Tested in : Eplan Electric P8 2026 (maintainer's account and a fresh account)
// Author    : Justin Walz, Walz Engineering
// License   : MIT (see LICENSE in the repo root)
// ============================================================
//
// What it changes: your Eplan USER keyboard shortcuts (and nothing else).
// It REPLACES your whole shortcut set with the one in the file, so it offers
// to save your current shortcuts first. To undo, run this script again and
// choose the backup file it made.
//
// ChangeLog:
//--------------------------------------------------------------------------------------
// 2026-11-12   V1.0.0   First release.
//                       - Imports a shortcut-keys XML file after an optional backup.
//                       - Checks the result by exporting again and comparing.
//--------------------------------------------------------------------------------------

using System;
using System.Collections.Generic;
using System.Diagnostics;              // Process
using System.Drawing;                  // Color, Font, Size, Point
using System.IO;                       // File, Directory, Path
using System.Runtime.InteropServices;  // DllImport (dark title bar)
using System.Text.RegularExpressions;  // Regex
using System.Windows.Forms;            // Form, controls, dialogs
using Eplan.EplApi.ApplicationFramework;   // CommandLineInterpreter, ActionCallingContext
using Eplan.EplApi.Base;               // Settings: read Eplan's color scheme
using Eplan.EplApi.Scripting;          // The [Start] attribute

// ---------------------------------------------------------------
// Part 1: the script Eplan runs.
// ---------------------------------------------------------------
public class ImportShortcutKeys
{
    // Script version. Keep it the same as the Version line in the header above.
    public const string Version = "1.0.0";

    // The settings node that holds the keyboard shortcuts.
    private const string ShortcutNode = "USER.SYSTEM.GUI.Shortcuts";
    private const string Title = "Import shortcut keys";

    [Start]
    public void Run()
    {
        SkiChoice choice;
        using (SkiImportWindow window = new SkiImportWindow())
        {
            if (SkiTheme.ShowOverEplan(window) != DialogResult.OK)
            {
                return;                                  // Cancel: nothing happens.
            }
            choice = window.Choice;
        }

        // Read and check the file before touching anything.
        List<string> wanted;
        string problem = SkiFile.ReadShortcuts(choice.File, out wanted);
        if (problem != null)
        {
            SkiNotice.Show(Title, "That file cannot be used", problem);
            return;
        }

        // One last question, because this replaces the user's shortcuts.
        string question = "Eplan will replace your keyboard shortcuts with the " + wanted.Count + " shortcuts in the file.\r\n\r\n";
        question += choice.Backup ? "Your current shortcuts are saved first." : "No backup will be made.";
        if (!SkiNotice.Ask(Title, "Replace your shortcuts?", question))
        {
            return;
        }

        CommandLineInterpreter cli = new CommandLineInterpreter();

        // Step 1: the backup. If it fails we stop and change nothing.
        string backupFile = null;
        if (choice.Backup)
        {
            try
            {
                Directory.CreateDirectory(choice.BackupFolder);
                backupFile = Path.Combine(choice.BackupFolder, "ShortcutKeys_Backup_" + DateTime.Now.ToString("yyyy-MM-dd_HHmmss") + ".xml");
                ActionCallingContext export = new ActionCallingContext();
                export.AddParameter("node", ShortcutNode);
                export.AddParameter("XMLFile", backupFile);
                cli.Execute("XSettingsExport", export);
                if (!File.Exists(backupFile))
                {
                    throw new IOException("Eplan did not write the backup file.");
                }
            }
            catch (Exception ex)
            {
                SkiNotice.Show(Title, "The backup failed, so nothing was changed", ex.Message);
                return;
            }
        }

        // Step 2: the import.
        try
        {
            ActionCallingContext import = new ActionCallingContext();
            import.AddParameter("XmlFile", choice.File);
            import.AddParameter("Node", ShortcutNode);
            cli.Execute("XSettingsImport", import);
        }
        catch (Exception ex)
        {
            SkiNotice.Show(Title, "The import failed", ex.Message + (backupFile != null ? "\r\n\r\nYour backup: " + backupFile : ""));
            return;
        }

        // Step 3: check the result by exporting again and comparing with the file.
        string checkFile = Path.Combine(Path.GetTempPath(), "ShortcutKeys_Check.xml");
        bool matches = false;
        try
        {
            ActionCallingContext check = new ActionCallingContext();
            check.AddParameter("node", ShortcutNode);
            check.AddParameter("XMLFile", checkFile);
            cli.Execute("XSettingsExport", check);

            List<string> now;
            if (SkiFile.ReadShortcuts(checkFile, out now) == null)
            {
                matches = SkiFile.SameShortcuts(wanted, now);
            }
        }
        catch (Exception)
        {
            matches = false;
        }

        string backupLine = (backupFile != null) ? "\r\n\r\nBackup saved to:\r\n" + backupFile : "";
        if (matches)
        {
            SkiNotice.Show(Title, "Shortcuts imported",
                "Your Eplan shortcuts now match the file (" + wanted.Count + " shortcuts). If a shortcut does not respond, restart Eplan." + backupLine);
        }
        else
        {
            SkiNotice.Show(Title, "Imported, but please check",
                "Eplan ran the import, but the shortcuts it reports do not match the file. Try restarting Eplan and test a shortcut." + backupLine);
        }
    }
}

// What the user chose in the window.
public class SkiChoice
{
    public string File;
    public bool Backup;
    public string BackupFolder;
}

// ---------------------------------------------------------------
// Part 2: reading the XML file.
// ---------------------------------------------------------------
public static class SkiFile
{
    // Returns null when the file is fine, otherwise a plain-English problem.
    // The shortcuts are returned in "shortcuts".
    public static string ReadShortcuts(string path, out List<string> shortcuts)
    {
        shortcuts = new List<string>();
        if (string.IsNullOrEmpty(path) || !File.Exists(path))
        {
            return "The file was not found:\r\n" + path;
        }

        string xml;
        try
        {
            xml = File.ReadAllText(path);
        }
        catch (Exception ex)
        {
            return "The file could not be read: " + ex.Message;
        }

        if (xml.IndexOf("name=\"Shortcuts\"", StringComparison.Ordinal) < 0)
        {
            return "This file does not contain a shortcut-keys section. Choose a shortcut file exported from Eplan (for example ShortcutKeys_StreamDeck.xml).";
        }

        foreach (Match m in Regex.Matches(xml, "<Val>(.*?)</Val>"))
        {
            shortcuts.Add(m.Groups[1].Value);
        }
        if (shortcuts.Count == 0)
        {
            return "The shortcut-keys section in this file is empty.";
        }
        return null;
    }

    // True when both lists hold the same shortcuts, in any order.
    public static bool SameShortcuts(List<string> a, List<string> b)
    {
        if (a.Count != b.Count)
        {
            return false;
        }
        List<string> x = new List<string>(a);
        List<string> y = new List<string>(b);
        x.Sort(StringComparer.Ordinal);
        y.Sort(StringComparer.Ordinal);
        for (int i = 0; i < x.Count; i++)
        {
            if (x[i] != y[i])
            {
                return false;
            }
        }
        return true;
    }
}

// ---------------------------------------------------------------
// Part 3: the look. Follows Eplan's light or dark color scheme.
// ---------------------------------------------------------------
public static class SkiTheme
{
    [DllImport("dwmapi.dll")]
    private static extern int DwmSetWindowAttribute(IntPtr hwnd, int attribute, ref int value, int size);

    public static bool Dark = IsEplanDark();

    public static Color Back { get { return Dark ? Color.FromArgb(32, 32, 32) : Color.FromArgb(243, 243, 243); } }
    public static Color Fore { get { return Dark ? Color.FromArgb(240, 240, 240) : Color.FromArgb(26, 26, 26); } }
    public static Color Head { get { return Dark ? Color.FromArgb(98, 169, 235) : Color.FromArgb(15, 108, 189); } }
    public static Color Field { get { return Dark ? Color.FromArgb(45, 45, 45) : Color.White; } }
    public static Color Border { get { return Dark ? Color.FromArgb(90, 90, 90) : Color.FromArgb(160, 160, 160); } }
    public static Color Muted { get { return Dark ? Color.FromArgb(170, 170, 170) : Color.FromArgb(96, 96, 96); } }

    // Colors a window and everything on it.
    public static void Apply(Form form)
    {
        form.BackColor = Back;
        form.ForeColor = Fore;
        Style(form.Controls);
        form.HandleCreated += delegate { ColorTitleBar(form); };
    }

    private static void Style(Control.ControlCollection controls)
    {
        foreach (Control c in controls)
        {
            Button button = c as Button;
            TextBox box = c as TextBox;
            if (button != null)
            {
                button.FlatStyle = FlatStyle.Flat;
                button.FlatAppearance.BorderColor = Border;
                button.BackColor = Field;
                button.ForeColor = Fore;
                button.UseVisualStyleBackColor = false;
            }
            else if (box != null)
            {
                box.BorderStyle = BorderStyle.FixedSingle;
                box.BackColor = Field;
                box.ForeColor = Fore;
            }
        }
    }

    // Shows the window in front of Eplan, centered on it.
    public static DialogResult ShowOverEplan(Form form)
    {
        IntPtr eplan = IntPtr.Zero;
        try
        {
            eplan = Process.GetCurrentProcess().MainWindowHandle;
        }
        catch (Exception)
        {
        }

        if (eplan == IntPtr.Zero)
        {
            form.StartPosition = FormStartPosition.CenterScreen;
            return form.ShowDialog();
        }
        form.StartPosition = FormStartPosition.CenterParent;
        return form.ShowDialog(new SkiOwner(eplan));
    }

    private static void ColorTitleBar(Form form)
    {
        try
        {
            int useDark = Dark ? 1 : 0;
            if (DwmSetWindowAttribute(form.Handle, 20, ref useDark, 4) != 0)
            {
                DwmSetWindowAttribute(form.Handle, 19, ref useDark, 4);
            }
            int caption = Back.R | (Back.G << 8) | (Back.B << 16);    // Windows wants blue-green-red order
            int text = Fore.R | (Fore.G << 8) | (Fore.B << 16);
            DwmSetWindowAttribute(form.Handle, 35, ref caption, 4);
            DwmSetWindowAttribute(form.Handle, 36, ref text, 4);
        }
        catch (Exception)
        {
        }
    }

    // Eplan keeps its color scheme in USER.MF.GuiColorScheme: 0 = follow Windows, 1 = dark, 2 = light.
    private static bool IsEplanDark()
    {
        try
        {
            Settings settings = new Settings();
            int scheme = settings.GetNumericSetting("USER.MF.GuiColorScheme", 0);
            if (scheme == 1) { return true; }
            if (scheme == 2) { return false; }
            object value = Microsoft.Win32.Registry.GetValue(
                @"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize", "AppsUseLightTheme", 1);
            return (value is int) && ((int)value == 0);
        }
        catch (Exception)
        {
            return true;                       // Eplan's default is dark
        }
    }
}

// ShowDialog needs an owner in the form of IWin32Window. This wraps a window handle.
public class SkiOwner : IWin32Window
{
    private readonly IntPtr handle;

    public SkiOwner(IntPtr handle)
    {
        this.handle = handle;
    }

    public IntPtr Handle
    {
        get { return handle; }
    }
}

// ---------------------------------------------------------------
// Part 4: a small message / question window (used instead of MessageBox so it matches the theme).
// ---------------------------------------------------------------
public class SkiNotice : Form
{
    public static void Show(string title, string heading, string text)
    {
        using (SkiNotice window = new SkiNotice(title, heading, text, false))
        {
            SkiTheme.ShowOverEplan(window);
        }
    }

    public static bool Ask(string title, string heading, string text)
    {
        using (SkiNotice window = new SkiNotice(title, heading, text, true))
        {
            return SkiTheme.ShowOverEplan(window) == DialogResult.Yes;
        }
    }

    private SkiNotice(string title, string heading, string text, bool question)
    {
        Text = title;
        FormBorderStyle = FormBorderStyle.FixedDialog;
        MinimizeBox = false;
        MaximizeBox = false;
        ShowInTaskbar = false;
        ClientSize = new Size(480, 210);

        Label headingLabel = new Label();
        headingLabel.Text = heading;
        headingLabel.Font = new Font("Segoe UI", 12f, FontStyle.Bold);
        headingLabel.ForeColor = SkiTheme.Head;
        headingLabel.Location = new Point(18, 16);
        headingLabel.Size = new Size(444, 28);

        Label textLabel = new Label();
        textLabel.Text = text;
        textLabel.Location = new Point(18, 52);
        textLabel.Size = new Size(444, 110);

        Controls.Add(headingLabel);
        Controls.Add(textLabel);

        if (question)
        {
            Button yes = MakeButton("Yes", DialogResult.Yes, new Point(292, 170));
            Button no = MakeButton("No", DialogResult.No, new Point(378, 170));
            AcceptButton = no;                 // The safe choice is the default.
            CancelButton = no;
            Controls.Add(yes);
            Controls.Add(no);
        }
        else
        {
            Button ok = MakeButton("OK", DialogResult.OK, new Point(378, 170));
            AcceptButton = ok;
            CancelButton = ok;
            Controls.Add(ok);
        }
        SkiTheme.Apply(this);
    }

    private static Button MakeButton(string text, DialogResult result, Point location)
    {
        Button button = new Button();
        button.Text = text;
        button.DialogResult = result;
        button.Location = location;
        button.Size = new Size(80, 28);
        return button;
    }
}

// ---------------------------------------------------------------
// Part 5: the main window.
// ---------------------------------------------------------------
public class SkiImportWindow : Form
{
    private readonly TextBox fileBox = new TextBox();
    private readonly CheckBox backupCheck = new CheckBox();
    private readonly TextBox folderBox = new TextBox();
    private readonly Button folderBrowse = new Button();

    public SkiChoice Choice;

    public SkiImportWindow()
    {
        Text = "Import shortcut keys  v" + ImportShortcutKeys.Version;
        ClientSize = new Size(540, 300);
        FormBorderStyle = FormBorderStyle.FixedDialog;
        MinimizeBox = false;
        MaximizeBox = false;
        ShowInTaskbar = false;

        Label heading = new Label();
        heading.Text = "Import shortcut keys";
        heading.Font = new Font("Segoe UI", 12f, FontStyle.Bold);
        heading.ForeColor = SkiTheme.Head;
        heading.Location = new Point(18, 14);
        heading.Size = new Size(500, 28);

        Label intro = new Label();
        intro.Text = "Replaces your Eplan keyboard shortcuts with the set in a shortcut file. Your other settings are not touched.";
        intro.Location = new Point(18, 46);
        intro.Size = new Size(500, 36);

        AddLabel("Shortcut file", 18, 98);
        fileBox.Location = new Point(18, 118);
        fileBox.Size = new Size(412, 24);
        fileBox.Text = FindDefaultFile();
        Button fileBrowse = new Button();
        fileBrowse.Text = "Browse...";
        fileBrowse.Location = new Point(438, 116);
        fileBrowse.Size = new Size(84, 28);
        fileBrowse.Click += delegate
        {
            using (OpenFileDialog dialog = new OpenFileDialog())
            {
                dialog.Filter = "Shortcut files (*.xml)|*.xml|All files (*.*)|*.*";
                if (dialog.ShowDialog() == DialogResult.OK) { fileBox.Text = dialog.FileName; }
            }
        };

        backupCheck.Text = "Back up my current shortcuts first (recommended)";
        backupCheck.Checked = true;
        backupCheck.AutoSize = true;
        backupCheck.Location = new Point(18, 160);
        backupCheck.CheckedChanged += delegate
        {
            folderBox.Enabled = backupCheck.Checked;
            folderBrowse.Enabled = backupCheck.Checked;
        };

        AddLabel("Backup folder", 18, 190);
        folderBox.Location = new Point(18, 210);
        folderBox.Size = new Size(412, 24);
        folderBox.Text = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments), "EplanShortcutBackups");
        folderBrowse.Text = "Browse...";
        folderBrowse.Location = new Point(438, 208);
        folderBrowse.Size = new Size(84, 28);
        folderBrowse.Click += delegate
        {
            using (FolderBrowserDialog dialog = new FolderBrowserDialog())
            {
                if (dialog.ShowDialog() == DialogResult.OK) { folderBox.Text = dialog.SelectedPath; }
            }
        };

        Button go = new Button();
        go.Text = "Import";
        go.Location = new Point(344, 258);
        go.Size = new Size(84, 28);
        go.Click += OnImport;
        Button cancel = new Button();
        cancel.Text = "Cancel";
        cancel.DialogResult = DialogResult.Cancel;
        cancel.Location = new Point(438, 258);
        cancel.Size = new Size(84, 28);
        AcceptButton = go;
        CancelButton = cancel;

        Controls.AddRange(new Control[] { heading, intro, fileBox, fileBrowse, backupCheck, folderBox, folderBrowse, go, cancel });
        SkiTheme.Apply(this);
    }

    private void AddLabel(string text, int x, int y)
    {
        Label label = new Label();
        label.Text = text;
        label.Location = new Point(x, y);
        label.AutoSize = true;
        Controls.Add(label);
    }

    // Pre-fills the file box when the file is in a common place.
    private static string FindDefaultFile()
    {
        string name = "ShortcutKeys_StreamDeck.xml";
        string[] folders = new string[]
        {
            Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments),
            Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), "Downloads"),
            Environment.GetFolderPath(Environment.SpecialFolder.DesktopDirectory)
        };
        foreach (string folder in folders)
        {
            string candidate = Path.Combine(folder, name);
            if (File.Exists(candidate))
            {
                return candidate;
            }
        }
        return "";
    }

    private void OnImport(object sender, EventArgs e)
    {
        if (fileBox.Text.Trim().Length == 0)
        {
            SkiNotice.Show("Import shortcut keys", "Choose a shortcut file", "Click Browse and pick the shortcut file you want to import.");
            return;
        }
        if (backupCheck.Checked && folderBox.Text.Trim().Length == 0)
        {
            SkiNotice.Show("Import shortcut keys", "Choose a backup folder", "Pick a folder for the backup, or untick the backup box.");
            return;
        }
        Choice = new SkiChoice();
        Choice.File = fileBox.Text.Trim();
        Choice.Backup = backupCheck.Checked;
        Choice.BackupFolder = folderBox.Text.Trim();
        DialogResult = DialogResult.OK;
    }
}
