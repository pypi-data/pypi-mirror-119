import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';
import { ICommandPalette } from '@jupyterlab/apputils';
import { IMainMenu } from '@jupyterlab/mainmenu';
import { requestAPI } from './handler';
import { ITopBar } from 'jupyterlab-topbar';
import { Widget } from '@lumino/widgets';

/**
 * Initialization data for jupyterlab-gpustats server extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab-gpustats',
  autoStart: true,
  requires: [ITopBar, ICommandPalette, IMainMenu, IThemeManager],
  activate: async (
      app: JupyterFrontEnd,
      topBar: ITopBar,
  ) => {
    console.log('JupyterLab extension jupyterlab-gpustats is activated!');

    const gpuUtlWidget = new Widget();
    const gpuMemWidget = new Widget();
    const storageWidget = new Widget();

    update();
    topBar.addItem('storage', storageWidget);
    topBar.addItem('gpu_mem', gpuMemWidget);
    topBar.addItem('gpu_utl', gpuUtlWidget);

    setInterval(update, 5000);

    function update() {
      requestAPI<any>('metrics')
          .then(data => {
            gpuUtlWidget.node.textContent =
                'GPU: ' + data['gpu']['utilization.gpu'] + '%';
            gpuMemWidget.node.textContent =
                'GPU Mem: ' +
                data['gpu']['memory.used'] +
                ' of ' +
                data['gpu']['memory.total'] +
                'MB';
            storageWidget.node.textContent =
                'Storage Used ' +
                data['storage']['used'] +
                ' / ' +
                data['storage']['free'] + ' Free';
          })
          .catch(reason => {
            console.error(
                `The jupyterlab_gpustats_service_info server extension appears to be missing.\n${reason}`
            );
          });
    }

  }
};

export default extension;
