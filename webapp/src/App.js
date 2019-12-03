import React from 'react';
import { HashRouter, Route, Switch } from 'react-router-dom';
import styled, { withTheme } from 'styled-components';
import Layout from './components/Layout';
import Home from './components/Home';
import WIP from './components/WIP';
import ModelDetail from './components/ModelDetail';
import ActionMenu from './components/ActionMenu';
import NotFoundPage from './components/NotFoundPage';
import ErrorCatching from './components/ErrorCatching';
import ModelBuilder from './components/ModelBuilder';

const Wrapper = styled('div')`
  background: ${(props) => props.theme.background};
  width: 100vw;
  height: 100vh;
  font-family: -apple-stem, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen";
  h1 {
    color: ${(props) => props.theme.body};
  }
`;

function App() {
  return (
    <Wrapper>
      <HashRouter>
        <Layout>
          <Switch>
            <Route exact path="/" component={Home} />
            <Route exact path="/wip" component={WIP} />
            <Route exact path="/models/props/:id" component={ModelDetail} />
            <Route exact path="/models/menu/:id" component={ActionMenu} />
            <Route exact path="/errorCatching" component={ErrorCatching} />
            <Route component={NotFoundPage} />
            <Route exact path="/modelcreator" component={ModelBuilder} />
          </Switch>
        </Layout>
      </HashRouter>
    </Wrapper>
  );
}

export default withTheme(App);
