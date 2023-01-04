//FUNCIONA CHAMANDO A FUNÇÃO CONFIGURAINT(), VOU USAR ESTA
function nivelInt(nivel){
    const puppeteer = require('puppeteer');

    async function apagaINT(page, num) {
        //acessa a apliccacao INT
        // console.log('#nav > a:nth-child('+num+')');
         await page.waitFor('#nav > a:nth-child('+num+')');
         await page.click('#nav > a:nth-child('+num+')');

         await page.waitFor('#ov-int-app-main > div.int-app-main-intents > div.summary-list > div.table-body > table > tbody > tr > td:nth-child(1)'),
         await page.click('#ov-int-app-main > div.int-app-main-intents > div.summary-list > div.table-body > table > tbody > tr > td:nth-child(1)')
        
         await page.waitFor('#ov-int-app-main > div.int-app-main-intents > div.tabular-header > div > div:nth-child(2) > svg'),
         await page.click('#ov-int-app-main > div.int-app-main-intents > div.tabular-header > div > div:nth-child(2) > svg')
        
        
         //console.log("Fim do configuraINT()");
        
        }


    
       
   (async() => {
     const browser = await puppeteer.launch({headless: false});
     const page = await browser.newPage();
     await page.goto('http://localhost:8181/onos/ui/login.html');
   
     //logar no site
     await page.type('#username','onos');
     await page.type('#password','rocks');
     await Promise.all([
       page.waitForNavigation(),
       page.click('#submit'),
      
     ]);
       
     //Acessa a barra de pesquisa
     await page.waitFor('#mast > span');
     await page.click('#mast > span');
   
      //const elemText = await page.$eval('#nav > a:nth-child(14)', elem => elem.innerText);
      const elemText = await page.$eval('#nav > a:nth-child(14)', elem => elem.textContent);
   
      if(elemText == ' In-band Telemetry Control'){
         //console.log('element innerText 14:', elemText);
         const num = 14
         //await configuraINT(page, num);  
         await apagaINT(page,num);
      }else{
           //console.log('element innerText 15:', elemText);
           const num = 15
           //await configuraINT(page, num);
           await apagaINT(page,num);
           }
   
      await browser.close();
   
    })()
   }//função para passar argumentos
   
   nivelInt(process.argv[2]);
   
