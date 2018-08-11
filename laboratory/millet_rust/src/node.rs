// This is node of chain. All logics should run here.

//use std::fs;
//use std::path::Path;
//use std::sync::Arc;
//use std::time::{SystemTime, UNIX_EPOCH};

extern crate tokio_reactor as Reactor;

pub fn run() -> Result<(), String> {

    let _event_loop = Reactor::Reactor::new();

    Ok(())
}