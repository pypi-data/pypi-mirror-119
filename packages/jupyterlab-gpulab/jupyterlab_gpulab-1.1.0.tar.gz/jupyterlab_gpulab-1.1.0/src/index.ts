import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ICommandPalette } from '@jupyterlab/apputils';
import { IMainMenu } from '@jupyterlab/mainmenu';
import { Toolbar } from '@jupyterlab/apputils';
import { Widget } from '@lumino/widgets';
import { Menu } from '@lumino/widgets';

/**
 * Initialization data for jupyterlab-gpulab server extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: "jupyterlab-gpulab",
  autoStart: true,
  requires: [ICommandPalette, IMainMenu],
  activate: async (
    app: JupyterFrontEnd,
    palette: ICommandPalette,
    mainMenu: IMainMenu
  ) => {
    document.title = "GPULab | JupyterLab Environment";

    const header = new Toolbar();
    header.id = 'gpulab-header'
    header.addClass('jp-gpulab-header')

    const logoWidget = new Widget();
    logoWidget.id = 'gpulab-logo'
    logoWidget.addClass('jp-gpulab-logo')

    header.addItem("logo", logoWidget);
    header.addItem("spacer", Toolbar.createSpacerItem());

    app.shell.add(header, 'header', undefined);

    const {commands} = app;
    const portal_command = 'gpulab:launch_portal';
    const blog_command = 'gpulab:launch_blog';
    const faq_command = 'gpulab:launch_faq';
    const contact_command = 'gpulab:launch_contact';
    const twitter_command = 'gpulab:twitter';
    const github_command = 'gpulab:github';

    commands.addCommand(portal_command, {
      label: 'GPULab Account Portal',
      caption: 'Open the GPULab portal.',
      execute: (args: any) => {
        window.open(`https://portal.gpulab.io`, 'gpulab-external');
      }
    });

    commands.addCommand(blog_command, {
      label: 'GPULab Blog',
      caption: 'Open the GPULab blog/',
      execute: (args: any) => {
        window.open(`https://gpulab.io/blog/`, 'gpulab-external');
      }
    });

    commands.addCommand(faq_command, {
      label: 'GPULab FAQ',
      caption: 'Open the GPULab FAQ page.',
      execute: (args: any) => {
        window.open(`https://gpulab.io/faq/`, 'gpulab-external');
      }
    });

    commands.addCommand(contact_command, {
      label: 'GPULab Contact',
      caption: 'Open the GPULab contact page.',
      execute: (args: any) => {
        window.open(`https://gpulab.io/blog/`, 'gpulab-external');
      }
    });

    commands.addCommand(twitter_command, {
      label: 'GPULab Twitter',
      caption: 'Follow GPULab on Twitter.',
      execute: (args: any) => {
        window.open(`https://twitter.com/gpulabio`, 'gpulab-external');
      }
    });

    commands.addCommand(github_command, {
      label: 'GPULab GitHub',
      caption: 'GPULab GitHub repository.',
      execute: (args: any) => {
        window.open(`https://github.com/gpulab`, 'gpulab-external');
      }
    });

    const category = 'GPULab';

    palette.addItem({command: portal_command, category: category, args: {}});
    palette.addItem({command: blog_command, category: category, args: {}});
    palette.addItem({command: faq_command, category: category, args: {}});
    palette.addItem({command: contact_command, category: category, args: {}});


    // Create a GPULab Menu
    const gpuLabMenu: Menu = new Menu({ commands });
    gpuLabMenu.title.label = 'GPULab';
    mainMenu.addMenu(gpuLabMenu, { rank: 1000 });

    gpuLabMenu.addItem({ command: portal_command, args: {}});
    gpuLabMenu.addItem({ command: blog_command, args: {}});
    gpuLabMenu.addItem({ command: faq_command, args: {}});
    gpuLabMenu.addItem({ command: contact_command, args: {}});
    gpuLabMenu.addItem({ command: twitter_command, args: {}});
    gpuLabMenu.addItem({ command: github_command, args: {}});

  }
};

export default extension;
