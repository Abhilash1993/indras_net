import React, { Component } from 'react';
import { HashRouter, Route, Switch } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './components/Home';
import WIP from './components/WIP';
import ModelDetail from './components/ModelDetail'
import MenuList from "./components/MenuList"
import Action from "./components/Action"
import NotFoundPage from './components/NotFoundPage';

class App extends Component {
  render() {
    return (
      <HashRouter>
        <Layout>
          <Switch>
            <Route exact path="/" component={Home} />
            <Route exact path="/wip" component={WIP} />
            <Route exact path="/models/props/" component={ModelDetail} />
            <Route exact path="/models/menu/" component={MenuList} />
            <Route exact path="/models/menu/" component={Action} />
            <Route component={NotFoundPage} />
          </Switch>
        </Layout>
      </HashRouter>
    );
  }
}

export default App;